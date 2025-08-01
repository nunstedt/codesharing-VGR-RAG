# Large Model Setup - macOS with Interface

This directory contains the large model implementation optimized for macOS systems with Streamlit web interface. It combines the enhanced capabilities of large models with a user-friendly web interface for production deployment.

## Features

- **macOS optimized** configuration and performance tuning
- **Streamlit web interface** for intuitive user interaction
- **Large model capabilities** for enhanced accuracy and reasoning
- **Multi-page web application** with dedicated functional areas
- **Production-ready** interface with visual system management

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

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run Overview.py
   ```

5. **Access the interface:**
   Open your browser to `http://localhost:8501`

## Files and Directories

### Web Interface Components
- **`Overview.py`** - Main Streamlit application entry point with macOS-optimized styling
- **`.streamlit/`** - Streamlit configuration directory for macOS-specific settings
- **`pages/`** - Directory containing individual Streamlit pages:
  - **`1_My_systems.py`** - System profile management interface
  - **`2_Compliance_assistant.py`** - Interactive compliance guidance with enhanced model reasoning
  - **`3_Regulation_navigation.py`** - Advanced regulation browsing with large model search
  - **`4_Add_system.py`** - Comprehensive system profile creation wizard

### Core Application Files
- **`main.py`** - Main entry point with large model configuration
- **`config.py`** - Configuration management optimized for macOS and large models
- **`mode_logic.py`** - Application mode handling (Profile, Compliance, QA)
- **`data_init.py`** - Data initialization and vector index creation

### Profile and Session Management
- **`profile_manager.py`** - Advanced system profile creation and management
- **`system_user_profile.py`** - Enhanced profile data structures
- **`chat_session.py`** - Chat session management for web interface
- **`chat_memory.py`** - Advanced conversation history and context management

### Query Processing
- **`query_handler.py`** - Core query processing with large model optimization
- **`query_metadata_extractor.py`** - Enhanced query analysis and metadata extraction
- **`prompt_assistant.py`** - Advanced prompt engineering for compliance assistance
- **`prompt_QA.py`** - Sophisticated prompt engineering for Q&A mode

### Data Processing and Retrieval
- **`index.py`** - Optimized vector store operations for large models
- **`ingest.py`** - Advanced document ingestion and preprocessing
- **`LLM.py`** - Large Language Model interface with macOS optimizations
- **`reranker.py`** - Enhanced search result reranking

### Model and Embedding
- **`embedding_data.py`** - Advanced embedding data utilities
- **`embedding_ft.py`** - Fine-tuning utilities optimized for large models
- **`model_onnx_export.py`** - ONNX model export for performance optimization

### Configuration and Build
- **`docker-compose.yaml`** - Docker services optimized for macOS with large model support
- **`Makefile`** - Build automation with macOS-specific optimizations
- **`requirements.txt`** - Python dependencies including Streamlit and large model requirements
- **`pyproject.toml`** - Python project configuration for large model setup
- **`.env`** - Environment variables (API keys, service URLs, model configurations)

### Data Directories
- **`data/`** - Processed document chunks optimized for large model retrieval
- **`chunks_test/`** - Test document chunks for development and validation
- **`pdf_folder/`** - Source PDF documents for ingestion
- **`unprocessed_pdf_folder/`** - PDF documents pending processing
- **`training_data/`** - Data for large model training and fine-tuning
- **`system_profile/`** - Stored system profile configurations
- **`local_qdrant_data/`** - Local Qdrant vector database storage

### Documentation and Analysis
- **`MODULE_STRUCTURE.md`** - Detailed module dependency graph and call flow
- **`ADDITIONAL_REFACTORING_ANALYSIS.md`** - Code refactoring analysis
- **`REFACTORING_NOTES.md`** - Implementation improvement notes
- **`README_extra.md`** - Additional documentation and usage examples
- **`LICENSE`** - Project license information

### Legacy Files
- **`main_prompt_old.py`** - Previous prompt handling version (deprecated)
- **`db.csv`** - Legacy CSV database for metadata

## Web Interface Pages

### 1. Overview (Main Page)
Enhanced landing page with:
- **Large model status indicators**
- **Performance metrics display**
- **Advanced navigation with model capabilities**

### 2. My Systems
- **Visual system profile management** with enhanced display
- **Advanced system selection** with model-powered recommendations
- **Comprehensive profile editing** with validation

### 3. Compliance Assistant
- **Enhanced chat interface** leveraging large model reasoning
- **Advanced system-specific guidance** with nuanced understanding
- **Contextual responses** with improved accuracy and depth

### 4. Regulation Navigation
- **Intelligent browsing** with large model-powered search
- **Advanced content analysis** and categorization
- **Enhanced search capabilities** with semantic understanding

### 5. Add System
- **Comprehensive profile creation** with intelligent guidance
- **Advanced validation** using large model reasoning
- **Dynamic questioning** that adapts based on responses

## macOS Optimizations

### Large Model Performance
- **Memory management** optimized for large models on macOS
- **Process scheduling** leveraging macOS performance cores
- **GPU acceleration** support for Apple Silicon (where applicable)

### Streamlit Configuration
- **macOS-specific theming** and styling
- **Performance optimizations** for large model responses
- **Memory management** for web interface with large models

### Docker Integration
- **Optimized container configurations** for macOS with large models
- **Volume mounts** configured for optimal I/O performance
- **Network settings** tuned for large model service communication

## Environment Setup

Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Model Configuration

<!-- QUESTION: What specific large model is configured for this interface version? Should this be different from the terminal version? -->

This setup uses large, high-capability models optimized for:
- **Complex reasoning** in web interface contexts
- **Enhanced user experience** with more accurate responses
- **Better handling** of multi-turn conversations
- **Improved context** understanding for web-based interactions

## Performance Considerations

- **Initial load time** may be longer due to large model initialization
- **Response times** optimized for web interface expectations
- **Memory usage** higher than standard interface version
- **Enhanced accuracy** and reasoning quality throughout the interface

## Development vs Production

This setup is designed for:
- **Production deployment** with high-quality responses
- **User-facing applications** requiring maximum accuracy
- **Complex compliance scenarios** needing advanced reasoning

For development and testing, consider the standard `interface/` directory for faster iteration.