"""Chat session handling for different modes."""

from llama_index.core import VectorStoreIndex
from chat_memory import CustomRAGChatEngine
from query_handler import (
    detect_language, 
    handle_chat_commands,
    execute_query_with_fallback,
    display_response
)
import streamlit as st

# For debugging purposes
from IPython import embed


class ChatSession:
    """Base class for chat sessions."""
    
    def __init__(self, vector_index: VectorStoreIndex, known_titles: list[str], max_history_turns: int = 4):
        self.vector_index = vector_index
        self.known_titles = known_titles
        self.max_history_turns = max_history_turns
    
    def create_chat_engine(self) -> CustomRAGChatEngine:
        """Create a new chat engine instance."""
        return CustomRAGChatEngine(self.vector_index, self.known_titles, max_history_turns=self.max_history_turns)
    
    def process_question(self, question: str, chat_engine: CustomRAGChatEngine) -> tuple[str, dict, dict]:
        """Process a question and return language, filters, and custom prompts."""
        # Detect language
        language = detect_language(question)
        print(f"\n\n+ The following language was detected:\n {language}")
        
        # Metadata filtering is now handled in the chat engine using the enhanced query
        filters = None
        
        return language, filters, {}
    
    
    def handle_question(self, question: str, chat_engine: CustomRAGChatEngine) -> bool:
        """Handle a single question. Returns False if session should end."""
        # Handle special commands
        if handle_chat_commands(question, chat_engine):
            return question.lower() not in ["exit", "quit"]
        
        # Process the question
        language, filters, custom_prompts = self.process_question(question, chat_engine)
        
        # Execute query
        response = execute_query_with_fallback(
            chat_engine, question, filters, custom_prompts, self.vector_index
        )
        
        # Display results
        display_response(response)
        
        return True
    
    def get_response(self, question: str, chat_engine: CustomRAGChatEngine):
        """Return the raw response object, without printing anything."""
        language, filters, custom_prompts = self.process_question(question, chat_engine)

        response = execute_query_with_fallback(
            chat_engine, question, filters, custom_prompts, self.vector_index
        
        )
        st.write("Custom prompts passed to LLM:")
        st.json(custom_prompts)

        st.write("Filters:")
        st.json(filters)

        return response


class ComplianceChatSession(ChatSession):
    """Chat session for compliance mode with system context."""
    
    def __init__(self, vector_index: VectorStoreIndex, known_titles: list[str], 
                 system_summary: str, max_history_turns: int = 5):
        super().__init__(vector_index, known_titles, max_history_turns)
        self.system_summary = system_summary
    
    def process_question(self, question: str, chat_engine: CustomRAGChatEngine) -> tuple[str, dict, dict]:
        """Process question with system context for compliance mode."""
        language, filters, _ = super().process_question(question, chat_engine)
        
        # Get compliance-specific prompt templates
        import prompt_assistant
        
        text_qa_template = prompt_assistant.get_text_qa_template().partial_format(
            language=language, 
            system_descr=self.system_summary
        )
        refine_template = prompt_assistant.get_refine_template().partial_format(
            language=language, 
            system_descr=self.system_summary
        )
        
        custom_prompts = {
            "response_synthesizer:text_qa_template": text_qa_template,
            "response_synthesizer:refine_template": refine_template,
        }
        
        return language, filters, custom_prompts


class QAChatSession(ChatSession):
    """Chat session for general Q&A mode."""
    
    def process_question(self, question: str, chat_engine: CustomRAGChatEngine) -> tuple[str, dict, dict]:
        """Process question for general Q&A mode."""
        language, filters, _ = super().process_question(question, chat_engine)
        
        # Get Q&A-specific prompt templates
        import prompt_QA
        
        text_qa_template = prompt_QA.get_text_qa_template().partial_format(language=language)
        refine_template = prompt_QA.get_refine_template().partial_format(language=language)

        # # For debugging purposes
        # print("QA session")
        # embed()
        
        custom_prompts = {
            "response_synthesizer:text_qa_template": text_qa_template,
            "response_synthesizer:refine_template": refine_template,
        }
        
        return language, filters, custom_prompts
