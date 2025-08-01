# Main - Terminal RAG Application

This is the core terminal-based implementation of the RAG (Retrieval-Augmented Generation) system for compliance and regulation assistance. This version uses small models optimized for quick research and development.

## Features

- **Terminal-only interface** for fast interaction
- **Small model setup** (gemini-2.5-flash) for quicker responses
- **English-only responses** 
- **Three operational modes:**
  - Profile Mode: Create and manage system profiles
  - Compliance Mode: System-specific compliance assistance
  - Q&A Mode: General regulation questions

## Quick Start

1. **Prerequisites:**
   - Python 3.12+
   - Docker installed and running
   - Google API key set as environment variable

2. **Setup Docker services:**
   ```bash
   make up
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Files and Directories

### Core Application Files
- **`main.py`** - Main entry point; orchestrates the application flow and user interaction
- **`config.py`** - Configuration management including LLM setup and environment variables
- **`mode_logic.py`** - Handles the three application modes (Profile, Compliance, QA)
- **`data_init.py`** - Initializes data ingestion and creates vector indexes

### Profile and Session Management
- **`profile_manager.py`** - Manages system profile creation and selection
- **`system_user_profile.py`** - Data structures for user and system profiles
- **`chat_session.py`** - Base chat session classes for different interaction modes
- **`chat_memory.py`** - Manages conversation history and context

### Query Processing
- **`query_handler.py`** - Core query processing and response coordination
- **`query_metadata_extractor.py`** - Extracts metadata and context from user queries
- **`prompt_assistant.py`** - Prompt engineering for compliance assistance mode
- **`prompt_QA.py`** - Prompt engineering for general Q&A mode

### Data Processing and Retrieval
- **`index.py`** - Vector store operations and similarity search
- **`ingest.py`** - Document ingestion, chunking, and preprocessing
- **`LLM.py`** - Large Language Model interface and configuration
- **`reranker.py`** - Search result reranking for improved relevance

### Configuration and Build
- **`docker-compose.yaml`** - Docker services configuration (Qdrant, embeddings, reranker)
- **`Makefile`** - Build automation (Docker services up/down)
- **`pyproject.toml`** - Python project configuration and dependencies
- **`.env`** - Environment variables (API keys, service URLs)

### Data Directories
- **`data/`** - Processed document chunks ready for indexing
- **`chunks_test/`** - Test document chunks for development
- **`pdf_folder/`** - Source PDF documents for ingestion
- **`pdf_folder_temp/`** - Temporary PDF processing directory
- **`unprocessed_pdf_folder/`** - PDF documents pending processing
- **`training_data/`** - Data for model training and fine-tuning
- **`system_profile/`** - Stored system profile configurations
- **`local_qdrant_data/`** - Local Qdrant vector database storage

### Legacy and Development Files
- **`main_prompt_old.py`** - Previous version of prompt handling (deprecated)
- **`embedding_data.py`** - Embedding data utilities
- **`embedding_ft.py`** - Fine-tuning utilities for embeddings
- **`db.csv`** - CSV database for metadata storage

### Documentation
- **`ADDITIONAL_REFACTORING_ANALYSIS.md`** - Analysis of code refactoring needs
- **`LICENSE`** - Project license information

## Docker Services

The application relies on Docker services defined in `docker-compose.yaml`:

- **Embedding Service** - Provides text embeddings using sentence-transformers/all-MiniLM-L6-v2
- **Reranker Service** - Improves search result relevance
- **Qdrant Database** - Vector database for storing document embeddings

## Environment Setup

Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage Modes

1. **Profile Mode**: Create system profiles by answering questions about your system/organization
2. **Compliance Mode**: Get compliance guidance specific to your system profile
3. **Q&A Mode**: Ask general questions about regulations and compliance

## Development Notes

This implementation prioritizes speed and simplicity for research purposes. For production use with web interface, see the `interface/` directory. For enhanced model performance, see `large-model-setups/`.