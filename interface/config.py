"""Configuration module for the RAG application."""

import os
from LLM import get_llm
from llama_index.core import Settings

# Model configuration
DEFAULT_MODEL_NAME = "gemini-2.5-flash"
DEFAULT_API_KEY = None #'AIzaSyDBy-fAy5xI8TbwnxndQggLFclCPdMvZ1w'

# Directory configuration
DEFAULT_DATA_DIR = "chunks_test"

def setup_llm(api_key=None, model_name=None):
    """Setup the LLM with the given API key and model name."""
    api_key = api_key or DEFAULT_API_KEY
    model_name = model_name or DEFAULT_MODEL_NAME
    
    # Set environment variable if API key is provided
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    Settings.llm = get_llm(api_key=api_key, model=model_name)
    return Settings.llm

def get_data_directory():
    """Get the data directory path."""
    return os.path.join(os.path.dirname(__file__), DEFAULT_DATA_DIR)
