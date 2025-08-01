"""Mode logic for the RAG application - refactored for better structure."""

from llama_index.core import VectorStoreIndex
from profile_manager import create_new_profile, select_system
from chat_session import ComplianceChatSession, QAChatSession


def run_profile_mode():
    """Run the profile creation mode."""
    create_new_profile()


def run_compliance_mode(vector_index: VectorStoreIndex, known_titles: list[str]):
    """Run the compliance mode with system-aware questions."""
    system_summary = select_system()
    if system_summary is None:
        return
    
    print("Ask questions about compliance related to your system (type exit to quit).\n")
    
    # Create and run compliance chat session
    chat_session = ComplianceChatSession(vector_index, known_titles, system_summary)
    chat_engine = chat_session.create_chat_engine()
    
    while True:
        question = input("Your question: ").strip()
        
        # Handle the question and check if we should continue
        should_continue = chat_session.handle_question(question, chat_engine)
        if not should_continue:
            break


def run_qa_mode(vector_index: VectorStoreIndex, known_titles: list[str]):
    """Run the general Q&A mode."""
    print("\nAsk anything to learn more about relevant regulations (type exit to quit).\n")
    
    # Create and run Q&A chat session
    chat_session = QAChatSession(vector_index, known_titles)
    chat_engine = chat_session.create_chat_engine()
    
    while True:
        question = input("Ask anything to learn more about relevant regulations: ").strip()
        
        # Handle the question and check if we should continue
        should_continue = chat_session.handle_question(question, chat_engine)
        if not should_continue:
            break