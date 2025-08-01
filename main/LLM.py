import os
from llama_index.llms.google_genai import GoogleGenAI

def get_llm(api_key=None, model="gemini-2.0-flash"):
    """
    Initialize and return a Google GenAI LLM instance.
    Args:
        api_key (str, optional): Google API key. If not provided, uses the GOOGLE_API_KEY env var.
        model (str, optional): Model name to use. Defaults to "gemini-2.0-flash".
    Returns:
        GoogleGenAI: Configured LLM instance.
    """
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    return GoogleGenAI(model=model)
