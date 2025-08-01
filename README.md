# codesharing-VGR-RAG

Codesharing after the Industrial Immersion Exchange program in collaboration with AI Sweden, Chalmers University of Technology, and Dakota State University.

This repository contains a Retrieval-Augmented Generation (RAG) system for compliance and regulation assistance, with multiple implementations to support different use cases and deployment scenarios.

## Directory Structure

### 📁 **main/**
Final prototype without interface - terminal-only interaction with small model setup for research purposes (faster execution). Provides English-only responses.
- **Run with:** `python main.py`
- **Use case:** Quick research and development, lightweight testing

### 📁 **interface/**
Full implementation WITH Streamlit web interface prototype for user-friendly interaction.
- **Run with:** `streamlit run Overview.py`
- **Use case:** Production-ready interface for end users

### 📁 **large-model-setups/**
Contains large model configurations for different platforms:
- **large-model-setup-mac/**: Large models optimized for macOS (terminal interface)
- **large-model-setup-interface-mac/**: Large models for macOS with interface
- **large-model-setup-windows/**: Large models optimized for Windows
- **Run with:** Same commands as main/interface respectively
- **Use case:** Enhanced performance with larger, more capable models

> **Note:** All folders contain similar code with small variations for model choices, interface options, and platform optimizations.

## Prerequisites & Setup

All implementations require Docker for running the database and embedding model services.

### Docker Setup
1. **Download and install Docker** from [docker.com](https://www.docker.com/)
2. **Start Docker** application
3. **Initialize services:** Run `make up` in your chosen directory

The Docker environment is defined in `docker-compose.yaml` and sets up:
- Vector database (Qdrant)
- Embedding model service
- Reranking service

## Module Structure

The following module structure applies to all non-interface folders (`main/`, `large-model-setups/*/`):

```
main.py                           # Entry point and application orchestration
├── config.py                     # Configuration management and LLM setup
├── data_init.py                  # Data initialization and index creation
└── mode_logic.py                 # Application mode handling (Profile/Compliance/QA)
    ├── profile_manager.py         # System profile creation and selection
    │   └── system_user_profile.py # Profile data structures
    └── chat_session.py            # Chat session management
        └── query_handler.py       # Query processing and response handling
            ├── chat_memory.py     # Conversation history management
            ├── query_metadata_extractor.py # Query analysis and metadata extraction
            ├── prompt_assistant.py # Prompt engineering for assistance mode
            ├── prompt_QA.py       # Prompt engineering for Q&A mode
            └── index.py           # Vector index operations

External Dependencies:
├── LLM.py                        # Large Language Model interface
├── ingest.py                     # Document ingestion and processing
├── reranker.py                   # Search result reranking
└── llama_index.*                 # Vector store and retrieval framework
```

### Interface Folder Additional Components
The `interface/` folder includes additional web interface components:
- **Overview.py**: Main Streamlit application entry point
- **pages/**: Directory containing individual Streamlit pages:
  - `1_My_systems.py`: System management interface
  - `2_Compliance_assistant.py`: Compliance guidance interface  
  - `3_Regulation_navigation.py`: Regulation browsing interface
  - `4_Add_system.py`: System addition interface

## Getting Started

1. Choose your implementation based on your needs
2. Navigate to the chosen directory
3. Set up Docker services: `make up`
4. Run the application using the respective command
5. Follow the interactive prompts or web interface

For detailed information about each implementation, see the README.md file in each respective directory.
