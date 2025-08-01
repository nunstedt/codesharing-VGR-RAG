# Interface - Streamlit Web Application

This directory contains the complete RAG system with a user-friendly Streamlit web interface for compliance and regulation assistance.

## Features

- **Web-based interface** using Streamlit for intuitive user interaction
- **Multi-page application** with dedicated sections for different functions
- **Visual system management** with easy profile creation and selection
- **Interactive compliance assistance** with contextual guidance
- **Regulation browsing** with search and filtering capabilities

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
   streamlit run Overview.py
   ```

4. **Access the interface:**
   Open your browser to `http://localhost:8501`

## Files and Directories

### Web Interface Components
- **`Overview.py`** - Main Streamlit application entry point with navigation and styling
- **`pages/`** - Directory containing individual Streamlit pages:
  - **`1_My_systems.py`** - System profile management interface
  - **`2_Compliance_assistant.py`** - Interactive compliance guidance with system context
  - **`3_Regulation_navigation.py`** - Browse and search through regulations
  - **`4_Add_system.py`** - System profile creation wizard

### Core Application Files (Same as main/)
- **`main.py`** - Main entry point; orchestrates the application flow
- **`config.py`** - Configuration management including LLM setup
- **`mode_logic.py`** - Handles application modes (Profile, Compliance, QA)
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

### Configuration and Dependencies
- **`docker-compose.yaml`** - Docker services configuration (Qdrant, embeddings, reranker)
- **`Makefile`** - Build automation (Docker services up/down)
- **`requirements.txt`** - Python dependencies including Streamlit
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

### Documentation and Analysis
- **`MODULE_STRUCTURE.md`** - Detailed module dependency graph and call flow
- **`ADDITIONAL_REFACTORING_ANALYSIS.md`** - Code refactoring analysis
- **`REFACTORING_NOTES.md`** - Notes on code improvements and structure
- **`README_extra.md`** - Additional documentation and usage notes
- **`LICENSE`** - Project license information

## Web Interface Pages

### 1. Overview (Main Page)
Landing page with navigation and system overview. Provides quick access to all application features.

### 2. My Systems
- View existing system profiles
- Select active system for compliance assistance
- Edit and manage system configurations

### 3. Compliance Assistant
- Interactive chat interface for compliance questions
- System-specific guidance based on selected profile
- Contextual responses considering your system's characteristics

### 4. Regulation Navigation
- Browse available regulations and standards
- Search through regulation content
- Access specific sections and requirements

### 5. Add System
- Step-by-step system profile creation wizard
- Guided questions to capture system characteristics
- Save profiles for future compliance assistance

## Docker Services

The application relies on Docker services defined in `docker-compose.yaml`:

- **Embedding Service** - Provides text embeddings using sentence-transformers models
- **Reranker Service** - Improves search result relevance
- **Qdrant Database** - Vector database for storing document embeddings

## Environment Setup

Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Development Notes

This interface implementation provides a production-ready web application for end-users. The Streamlit framework enables rapid development of interactive data applications with minimal frontend code.

For terminal-only usage, see the `main/` directory. For enhanced model performance, see `large-model-setups/`.