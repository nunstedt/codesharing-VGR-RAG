import argparse
from ingest import parse_and_get_nodes
from index import get_vector_index, get_retriever
import os
from LLM import get_llm
from llama_index.core import Settings
from contextlib import redirect_stdout
import time  # Add this import at the top with other imports
from mode_logic import run_mode

def main(chat_mode=False):
    # For debugging purposes


    # Insert your own Google API key here!!
    my_google_API_key = None #

    # Choose the model you want to use
    # Documentation: https://cloud.google.com/vertex-ai/generative-ai/docs/models
    # Rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
    # 2.0 models:
  


    print("\n--- Regulation Navigator ---")
    print("Available modes:")
    print(" 1. Profile  - Add and describe a system")
    print(" 2. Compliance assistant - Ask compliance questions based on your system responsibilities")
    print(" 3. QA       - Explore regulations freely")

    mode = input("\nEnter a mode: ").strip().lower()
    run_mode(mode)
    print(mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat", action="store_true", help="Run in interactive chat mode")
    args = parser.parse_args()
    main(chat_mode=args.chat)