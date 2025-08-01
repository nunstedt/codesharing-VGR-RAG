"""Main entry point for the RAG application."""

from config import setup_llm
from data_init import initialize_data_and_index
from mode_logic import run_profile_mode, run_compliance_mode, run_qa_mode
import os


# For debugging purposes
from IPython import embed

# Retrieve the Google API key from an environment variable
my_google_API_key = os.getenv("GOOGLE_API_KEY")

# models:
model_name = "gemini-2.5-flash"         # Our newest multimodal model, with next generation features and improved capabilities

# Known titles - ATM WE ONLY HAVE THESE TITLES DUE TO MISSING/DUPLICATE pdf_title METADATA
KNOWN_TITLES = {
    "Commission Guidelines on AI Prohibitions",
    "Critical Entity Resilience (CER)",
    "EU AI Act",
    "High Level Summary of the AI Act",
    "ISO 27002",
    "Medical Device Regulation (MDR)",
    "NIS2 Directive",
    "Policy för säkerhet och beredskap 2025-2029",
    "Protective Security Act"
}


def main():
    """Main function to run the RAG application."""
    # Setup LLM
    setup_llm(api_key=my_google_API_key, model_name=model_name)
    
    # Initialize data and vector index
    print("Initializing data and vector index...")
    _, _, vector_index = initialize_data_and_index()
    
    # Display menu and handle user choice
    print("\n--- Regulation Navigator ---")
    print("Available modes:")
    print(" 1. Profile  - Add and describe a system")
    print(" 2. Compliance assistant - Ask compliance questions based on your system responsibilities")
    print(" 3. QA       - Explore regulations freely")

    mode = input("\nEnter a mode: ").strip().lower()
    if mode == "1":
        run_profile_mode()
    elif mode == "2":
        run_compliance_mode(vector_index=vector_index, known_titles=KNOWN_TITLES)
    elif mode == "3":
        run_qa_mode(vector_index=vector_index, known_titles=KNOWN_TITLES)
    else:
        print("Invalid mode, please choose one of the modes above")


if __name__ == "__main__":
    main()

