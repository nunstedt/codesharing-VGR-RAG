# Large Model Setup - Windows (Terminal)

This directory contains the large model implementation optimized for Windows systems with terminal interface. It provides enhanced performance and capabilities compared to the lightweight version in the `main/` directory, with Windows-specific optimizations.

## Features

- **Windows optimized** configuration and paths
- **Terminal-only interface** for efficient interaction
- **Large model capabilities** for enhanced accuracy
- **Same three operational modes** as main: Profile, Compliance, Q&A
- **Windows-specific optimizations** for path handling and services

## Quick Start

1. **Prerequisites:**
   - Windows 10/11
   - Python 3.12+
   - Docker Desktop for Windows installed and running
   - Google API key set as environment variable

2. **Setup Docker services:**
   ```cmd
   make up
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```cmd
   python main.py
   ```

## Files and Directories

### Core Application Files
- **`main.py`** - Main entry point with large model configuration for Windows
- **`config.py`** - Configuration management optimized for Windows paths and settings
- **`mode_logic.py`** - Application mode handling (Profile, Compliance, QA)
- **`data_init.py`** - Data initialization and vector index creation

### Profile and Session Management
- **`profile_manager.py`** - System profile creation and management
- **`system_user_profile.py`** - Profile data structures with Windows compatibility
- **`chat_session.py`** - Chat session management for different interaction modes
- **`chat_memory.py`** - Conversation history and context management

### Query Processing
- **`query_handler.py`** - Core query processing and response coordination
- **`query_metadata_extractor.py`** - Query analysis and metadata extraction
- **`prompt_assistant.py`** - Prompt engineering for compliance assistance
- **`prompt_QA.py`** - Prompt engineering for general Q&A mode

### Data Processing and Retrieval
- **`index.py`** - Vector store operations and similarity search
- **`ingest.py`** - Document ingestion with Windows path handling
- **`LLM.py`** - Large Language Model interface with Windows optimizations
- **`reranker.py`** - Search result reranking for improved relevance

### Model and Embedding
- **`embedding_data.py`** - Embedding data utilities and management
- **`embedding_ft.py`** - Fine-tuning utilities for embeddings
- **`model_onnx_export.py`** - ONNX model export functionality for Windows optimization
- **`export_models/`** - Directory for exported model files and configurations

### Configuration and Build
- **`docker-compose.yaml`** - Docker services configuration optimized for Windows
- **`Makefile`** - Build automation with Windows-compatible commands
- **`requirements.txt`** - Python dependencies for large model setup on Windows
- **`pyproject.toml`** - Python project configuration
- **`.env`** - Environment variables (API keys, service URLs)

### Data Directories
- **`data/`** - Processed document chunks ready for indexing
- **`chunks_test/`** - Test document chunks for development and validation
- **`pdf_folder/`** - Source PDF documents for ingestion
- **`pdf_folder_temp/`** - Temporary PDF processing directory (Windows temp handling)
- **`unprocessed_pdf_folder/`** - PDF documents pending processing
- **`training_data/`** - Data for model training and fine-tuning
- **`system_profile/`** - Stored system profile configurations
- **`local_qdrant_data/`** - Local Qdrant vector database storage

### Documentation and Analysis
- **`MODULE_STRUCTURE.md`** - Detailed module dependency graph and call flow
- **`ADDITIONAL_REFACTORING_ANALYSIS.md`** - Code refactoring analysis and recommendations
- **`REFACTORING_NOTES.md`** - Notes on code improvements and structural changes
- **`README_extra.md`** - Additional usage documentation and Windows-specific examples
- **`LICENSE`** - Project license information

### Legacy Files
- **`main_prompt_old.py`** - Previous version of prompt handling (deprecated)
- **`db.csv`** - CSV database for metadata storage (legacy)

## Windows Optimizations

This implementation includes several Windows-specific optimizations:

### Path Handling
- **Windows-style path separators** (backslashes) properly handled
- **Drive letter support** for absolute paths
- **Long path support** for Windows systems with extended path length
- **Special character handling** in Windows filenames

### Docker Configuration
- **Docker Desktop for Windows** optimized settings
- **Windows container support** where applicable
- **Volume mounts** configured for Windows filesystem
- **Network configurations** appropriate for Windows Docker environment

### Performance Tuning
- **Memory management** optimized for Windows virtual memory system
- **Process handling** leveraging Windows process management
- **File I/O optimizations** for NTFS filesystem performance
- **Windows service integration** capabilities

### Environment Variables
- **Windows environment variable** handling
- **PowerShell compatibility** for advanced users
- **Windows registry integration** where needed

## Environment Setup

### Option 1: Command Prompt / PowerShell
Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### Option 2: System Environment Variables
Set via Windows System Properties:
- Variable: `GOOGLE_API_KEY`
- Value: `your_google_api_key_here`

## Model Configuration

<!-- QUESTION: What specific large model is configured here? Should this be different from the macOS versions for Windows-specific optimizations? -->

This setup is configured to use larger, more capable models optimized for Windows systems. The model selection provides:
- **Improved reasoning** for complex compliance scenarios
- **Better context understanding** for nuanced regulatory questions
- **Enhanced accuracy** in regulatory interpretation
- **Windows-optimized** model loading and memory management

## Usage Modes

1. **Profile Mode**: Create comprehensive system profiles through guided questions
2. **Compliance Mode**: Get detailed compliance guidance specific to your system
3. **Q&A Mode**: Ask complex questions about regulations with enhanced reasoning

## Performance Considerations

- **Response times** will be longer due to large model processing
- **Memory usage** optimized for Windows memory management
- **Disk I/O** optimized for NTFS filesystem performance
- **Better handling** of complex, multi-faceted compliance questions

## Windows-Specific Features

### Integration Capabilities
- **Windows service** deployment potential
- **Active Directory** integration possibilities
- **Windows security** model compatibility
- **Enterprise Windows** environment support

### Development Tools
- **Visual Studio Code** integration
- **PowerShell** script support
- **Windows Terminal** optimization
- **WSL compatibility** for hybrid development

## Troubleshooting

### Common Windows Issues
- **Path length limitations**: Enable long path support in Windows
- **Antivirus interference**: Add project directory to exclusions
- **Docker daemon**: Ensure Docker Desktop is running
- **Python path**: Verify Python is in system PATH

For faster development iteration, consider using the `main/` directory. For web interface capabilities, this Windows setup is terminal-only - consider the macOS interface versions for web UI needs.