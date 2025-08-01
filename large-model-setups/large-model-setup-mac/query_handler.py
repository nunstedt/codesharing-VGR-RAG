"""Query processing and handling functionality."""

from langdetect import detect
from llama_index.core.vector_stores import MetadataFilters
from chat_memory import CustomRAGChatEngine
from index import get_query_engine


def detect_language(question: str) -> str:
    """Detect the language of a question and return 'Swedish' or 'English'."""
    language = detect(question)
    return "Swedish" if language.startswith("sv") else "English"


def handle_chat_commands(question: str, chat_engine: CustomRAGChatEngine) -> bool:
    """Handle special chat commands like 'exit', 'quit', 'reset'. Returns True if command was handled."""
    if question.lower() in ["exit", "quit"]:
        return True
    elif question.lower() == "reset" and chat_engine:
        if hasattr(chat_engine, 'reset_memory'):
            chat_engine.reset_memory()
        elif hasattr(chat_engine, 'reset_conversation'):
            chat_engine.reset_conversation()
        print("🔄 Memory cleared!")
        return True
    return False


def execute_query_with_fallback(chat_engine: CustomRAGChatEngine, question: str, 
                              filters: MetadataFilters, custom_prompts: dict, vector_index):
    """Execute a query with chat engine, falling back to regular retrieval if needed."""
    try:
        # With memory chat - filters are now handled internally by the chat engine
        response = chat_engine.chat(question, filters=None, custom_prompts=custom_prompts)
        print(f"\n💬 Assistant with memory!")
        return response
    
    except Exception as e:
        # Without memory fallback
        print(f"❌ Error with memory chat: {e}")
        # print("Falling back to regular retrieval...")
        # # Fallback to original behavior
        # import prompt_assistant
        # query_engine = get_query_engine(vector_index, filters)
        # prompt_assistant.update_prompts(query_engine, custom_prompts)
        # response = query_engine.query(question)
        # print(f"\n💬 Assistant without memory!")
        # return response


def display_response(response) -> None:
    """Display the response and retrieved chunks."""
    print('Retrieved Chunks: ')
    if not response.source_nodes:
        print("\n No relevant information found in the documents.")
        return

    for i, node in enumerate(response.source_nodes):
        print(f"\n++ Chunk {i+1}:")
        print(node.text)

    print("\nThe tool provides the following answer:\n")
    print(response.response)
