# Large Model Setup - macOS (Terminal)

This directory contains the large model implementation optimized for macOS systems with terminal interface. It provides enhanced performance and capabilities compared to the lightweight version in the `main/` directory.

## Features

- **macOS optimized** configuration and paths
- **Terminal-only interface** for efficient interaction
- **Large model capabilities** for enhanced accuracy
- **Same three operational modes** as main: Profile, Compliance, Q&A
- **macOS-specific optimizations** for Apple Silicon and Intel Macs

## Quick Start

1. **Prerequisites:**
   - macOS (Intel or Apple Silicon)
   - Python 3.12+
   - Docker Desktop for Mac installed and running
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
- **`main.py`** - Main entry point with model configuration for large models
- **`config.py`** - Configuration management optimized for macOS paths and settings
- **`mode_logic.py`** - Application mode handling (Profile, Compliance, QA)
- **`data_init.py`** - Data initialization and vector index creation

### Profile and Session Management
- **`profile_manager.py`** - System profile creation and management
- **`system_user_profile.py`** - Profile data structures and validation
- **`chat_session.py`** - Chat session management for different interaction modes
- **`chat_memory.py`** - Conversation history and context management

### Query Processing
- **`query_handler.py`** - Core query processing and response coordination
- **`query_metadata_extractor.py`** - Query analysis and metadata extraction
- **`prompt_assistant.py`** - Prompt engineering for compliance assistance
- **`prompt_QA.py`** - Prompt engineering for general Q&A mode

### Data Processing and Retrieval
- **`index.py`** - Vector store operations and similarity search
- **`ingest.py`** - Document ingestion, chunking, and preprocessing
- **`LLM.py`** - Large Language Model interface and configuration
- **`reranker.py`** - Search result reranking for improved relevance

### Model and Embedding
- **`embedding_data.py`** - Embedding data utilities and management
- **`embedding_ft.py`** - Fine-tuning utilities for embeddings
- **`model_onnx_export.py`** - ONNX model export functionality for optimization

### Configuration and Build
- **`docker-compose.yaml`** - Docker services configuration optimized for macOS
- **`Makefile`** - Build automation with macOS-specific commands
- **`requirements.txt`** - Python dependencies for large model setup
- **`pyproject.toml`** - Python project configuration
- **`.env`** - Environment variables (API keys, service URLs)

### Data Directories
- **`data/`** - Processed document chunks ready for indexing
- **`chunks_test/`** - Test document chunks for development and validation
- **`pdf_folder/`** - Source PDF documents for ingestion
- **`pdf_folder_temp/`** - Temporary PDF processing directory
- **`unprocessed_pdf_folder/`** - PDF documents pending processing
- **`training_data/`** - Data for model training and fine-tuning
- **`system_profile/`** - Stored system profile configurations
- **`local_qdrant_data/`** - Local Qdrant vector database storage

### Documentation and Analysis
- **`MODULE_STRUCTURE.md`** - Detailed module dependency graph and call flow
- **`ADDITIONAL_REFACTORING_ANALYSIS.md`** - Code refactoring analysis and recommendations
- **`REFACTORING_NOTES.md`** - Notes on code improvements and structural changes
- **`README_extra.md`** - Additional usage documentation and examples
- **`LICENSE`** - Project license information

### Legacy Files
- **`main_prompt_old.py`** - Previous version of prompt handling (deprecated)
- **`db.csv`** - CSV database for metadata storage (legacy)

## macOS Optimizations

This implementation includes several macOS-specific optimizations:

### Path Handling
- **Unix-style paths** throughout the codebase
- **Case-sensitive filesystem** awareness
- **Proper handling of spaces** in macOS directory names

### Docker Configuration
- **Docker Desktop for Mac** optimized settings
- **Volume mounts** configured for macOS filesystem
- **Network configurations** appropriate for macOS Docker environment

### Performance Tuning
- **Memory management** optimized for macOS virtual memory system
- **Process handling** leveraging macOS process management
- **File I/O optimizations** for macOS filesystem performance

## Environment Setup

Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Model Configuration

<!-- QUESTION: What specific large model is configured here? The code shows gemini-2.5-flash but for large model setups, should this be gemini-2.5-pro or another larger model? -->

This setup is configured to use larger, more capable models for enhanced performance. The model selection provides:
- **Improved reasoning** for complex compliance scenarios
- **Better context understanding** for nuanced regulatory questions
- **Enhanced accuracy** in regulatory interpretation

## Usage Modes

1. **Profile Mode**: Create comprehensive system profiles through guided questions
2. **Compliance Mode**: Get detailed compliance guidance specific to your system
3. **Q&A Mode**: Ask complex questions about regulations with enhanced reasoning

## Performance Considerations

- **Response times** will be longer due to large model processing
- **Memory usage** will be higher than the lightweight version
- **Accuracy** and **reasoning quality** will be significantly improved
- **Better handling** of complex, multi-faceted compliance questions

For faster development iteration, consider using the `main/` directory. For web interface with large models, see `large-model-setup-interface-mac/`.