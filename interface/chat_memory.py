from llama_index.core.chat_engine import SimpleChatEngine, CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilters
from typing import Any, List
from index import get_query_engine
import time
from reranker import TEIReranker

from llama_index.core.prompts import RichPromptTemplate
from llama_index.core.prompts import PromptTemplate

from prompt_assistant import update_prompts  # Fixed import
from LLM import get_llm
from llama_index.core import Settings

from IPython import embed

# Import metadata filtering functions to avoid circular imports
from query_metadata_extractor import extract_metadata_filters, validate_metadata_filters
from llama_index.core.vector_stores import FilterCondition

# Remove hardcoded configuration - use config.py instead
reranker = TEIReranker("http://localhost:5081")


class CustomRAGChatEngine:
    """
    Custom RAG chat engine with memory, enhanced query context,
    and Google GenAI–powered summarization of old turns.
    """

    def __init__(self, vector_index: VectorStoreIndex, known_titles: List[str], max_history_turns: int):
        self.vector_index = vector_index
        self.known_titles = known_titles
        self.max_history_turns = max_history_turns
        self.conversation_history = []
        # Create an LLMPredictor once, tied to your Settings.llm

    def _format_history_for_context(self) -> str:
        """Format history (including any summary) into a single context string."""
        if not self.conversation_history:
            return ""

        lines = []
        for turn in self.conversation_history:
            if "summary" in turn:
                lines.append(f"Summary of earlier conversation: {turn['summary']}")
            else:
                lines.append(f"Human: {turn['user']}")
                lines.append(f"Assistant: {turn['assistant']}")
        return "\n".join(lines)

    def _process_metadata_filters(self, question: str, cutoff: float = 0.75) -> MetadataFilters:
        """Process and validate metadata filters for a question."""
        # 1) Ask Gemini to normalize:
        raw_filters = extract_metadata_filters(question, self.known_titles)

        # 2) Fuzzy‑validate / canonicalize:
        filters_no_or = validate_metadata_filters(raw_filters, self.known_titles, cutoff=cutoff)

        # 3) Log any remapping:
        for f_raw, f_final in zip(raw_filters.filters, filters_no_or.filters):
            if f_raw.value != f_final.value:
                print(f"[INFO] LLM gave '{f_raw.value}', mapped → '{f_final.value}'")

        # 4) Combine with OR so *any* title match will return chunks:
        return MetadataFilters(
            filters=filters_no_or.filters,
            condition=FilterCondition.OR
        )

    def _enhance_query(self, query: str) -> str:
        # Return early if nothing to work with
        if not self.conversation_history:
            print("[DEBUG] Skipping enhancement: no history")
            return query

        last_turns: list[str] = []
        max_ctx_turns = min(3, self.max_history_turns)

        # Walk backwards, but only count real Q‑A pairs
        print("[DEBUG] Memory passed into enhancer:")
        for turn in reversed(self.conversation_history):
            if "user" in turn and "assistant" in turn:
                last_turns.extend(
                    [f"Human: {turn['user']}",
                    f"Assistant: {turn['assistant']}"]
                )
            elif "summary" in turn:
                last_turns.append(f"Earlier conversation summary: {turn['summary']}")

            # stop when we have enough lines from full turns
            if len([t for t in last_turns if t.startswith("Human:")]) >= max_ctx_turns:
                break
        conversation_str = "\n".join(last_turns)

        print("[DEBUG] Condensation prompt:")
        print(f"Conversation:\n{conversation_str}")
        print(f"Latest user query:\n{query}")

        # Attempt LLM-based condensation
        try:
            condense_prompt = f"""Given the conversation so far, rewrite the latest user message 
            into a standalone question for document retrieval.

            Conversation:
            {conversation_str}

            Latest user message: {query}

            Standalone query:"""


            small_llm = get_llm(model="gemini-2.5-flash")
            condensed_query = small_llm.complete(prompt=condense_prompt, temperature=0.2, max_tokens=100).text.strip()            

            print(f"[DEBUG] Gemini returned condensed query: {condensed_query!r}")
            # Fallback if the response is empty or too short
            if not condensed_query or len(condensed_query.split()) < 2:
                print("[DEBUG] Condensed query too short, falling back to original")
                condensed_query = query
            return condensed_query

        except Exception as e:
            print(f"[WARN] Condensing query failed: {e}. Falling back to heuristic.")
            last_qs = [t["user"] for t in self.conversation_history[-2:]]
            return f"Context from recent Qs: {' | '.join(last_qs)}\nCurrent question: {query}"

    def _summarize_history(self):
        """
        When history exceeds max_history_turns, collapse all but the most recent
        turn into a 2–3 sentence summary via Google GenAI, then keep the latest turn.
        """
        keep_count = 1
        # Nothing to do if we have at most keep_count turns
        if len(self.conversation_history) <= keep_count:
            return

        # Split off the oldest turns and the turns to keep
        to_summarize = self.conversation_history[:-keep_count]
        to_keep = self.conversation_history[-keep_count:]

        # Build a string of the old turns
        old_history_str = "\n".join(
            f"Human: {t['user']}\nAssistant: {t['assistant']}"
            for t in to_summarize
            if "user" in t and "assistant" in t
        )

        # Summarize the old turns
        prompt_template = PromptTemplate(
            template="""
                You are a helpful assistant that concisely summarizes conversations.
                Summarize the following in 2 – 3 sentences:

                {history_str}
            """
        )
        summary = Settings.llm.predict(
            prompt_template,
            history_str=old_history_str
        ).strip()

        # Rebuild history: the most recent turn(s) + one summary
        self.conversation_history = to_keep + [
            {"user": "[system]", "assistant": summary}
        ]

    def chat(
        self,
        message: str,
        filters: MetadataFilters = None,
        custom_prompts: dict = None
    ) -> str:
        """
        Chat with memory-enhanced retrieval and auto-summarization.

        Args:
            message: User's message.
            filters: Optional MetadataFilters for retrieval. If None, will be extracted from enhanced query.
            custom_prompts: Optional dict of prompt templates to apply.

        Returns:
            The assistant's response text.
        """

        # Build the full prompt
        history_ctx = self._format_history_for_context()
        enhanced_q = self._enhance_query(message)
        print(f"[INFO] Condensed query: {enhanced_q}")

        # Process metadata filters using the enhanced query instead of original message
        # if filters is None:
        filters = self._process_metadata_filters(enhanced_q)
        print(f"[INFO] Using filters: {filters.filters}")
        # embed()
        # Retrieve + generate answer

        # print(f"\n+History context for retrieval:\n{history_ctx}")
        # print(f"\n+Enhanced query for retrieval:\n{enhanced_q}")
        # print(f"\n\n+ Full query for retrieval:\n {full_query}")
        

        custom_prompts["response_synthesizer:text_qa_template"] = (
        custom_prompts["response_synthesizer:text_qa_template"].partial_format(history_str=history_ctx)
        )

        custom_prompts["response_synthesizer:refine_template"] = (
        custom_prompts["response_synthesizer:refine_template"].partial_format(history_str=history_ctx)
        )


        # Always get a fresh query engine
        query_engine = get_query_engine(self.vector_index, filters)

        # Apply any custom prompts
        if custom_prompts:
            update_prompts(query_engine, custom_prompts)

        try:
            response = query_engine.query(enhanced_q)
            answer = str(response.response)
            # embed()
           # Print metadata of all retriever chunks for debugging:
            for node in response.source_nodes:
                print(f"[DEBUG] Retrieved chunk from: {node.metadata.get('pdf_title', 'No title found')}")
                
            # # Debug: Check if metadata is present in source nodes
            # if response.source_nodes:
            #     print(f"[DEBUG] Retrieved {len(response.source_nodes)} chunks")
            #     for i, node in enumerate(response.source_nodes[:3]):  # Show first 3
            #         title = node.metadata.get("pdf_title", "No title found")
            #         print(f"[DEBUG] Chunk {i+1} from: {title}")
            # # embed()


        except Exception as e:
            response = None
            print(f"[Error] Retrieval failed: {e}")

        # Add to memory
        self.conversation_history.append({"user": message, "assistant": answer})

        # If too many turns, summarize via GenAI
        if len(self.conversation_history) > self.max_history_turns:
            # print("YES!!!!!!!!!!!!!!!!!")
            # embed()
            self._summarize_history()

        return response

    def reset_conversation(self):
        """Clear all history and summary."""
        self.conversation_history = []