# Large Model Setups

This directory contains implementations optimized for large, high-performance language models across different platforms. These setups provide enhanced accuracy and capabilities compared to the lightweight versions in `main/` and `interface/`.

## Directory Overview

### 📁 **large-model-setup-mac/**
Large model implementation optimized for macOS systems with terminal interface.
- **Run with:** `python main.py`
- **Platform:** macOS optimized
- **Interface:** Terminal/command-line only
- **Use case:** High-performance research and development on Mac

### 📁 **large-model-setup-interface-mac/** 
Large model implementation for macOS with Streamlit web interface.
- **Run with:** `streamlit run Overview.py`
- **Platform:** macOS optimized
- **Interface:** Web-based Streamlit interface
- **Use case:** Production deployment on Mac with user-friendly interface

### 📁 **large-model-setup-windows/**
Large model implementation optimized for Windows systems.
- **Run with:** `python main.py`
- **Platform:** Windows optimized
- **Interface:** Terminal/command-line only
- **Use case:** High-performance deployment on Windows

## Key Differences from Main/Interface

### Model Configuration
- **Larger, more capable models** (e.g., gemini-2.5-pro instead of gemini-2.5-flash)
- **Enhanced reasoning capabilities** for complex compliance scenarios
- **Improved multilingual support** where applicable
- **Higher token limits** for longer context processing

### Performance Considerations
- **Increased response time** due to larger model processing
- **Higher memory requirements** for model operations
- **Enhanced accuracy** for complex regulatory questions
- **Better handling of nuanced compliance scenarios**

### Platform Optimizations
- **macOS versions** include optimizations for Apple Silicon and macOS-specific configurations
- **Windows version** includes Windows-specific path handling and service configurations
- **Docker configurations** tuned for each platform's capabilities

## Setup Instructions

1. **Choose your platform** and interface preference
2. **Navigate to the appropriate directory**
3. **Follow the setup instructions** in that directory's README.md
4. **Start Docker services:** `make up`
5. **Run the application** using the specified command

## When to Use Large Model Setups

Choose large model setups when you need:
- **Maximum accuracy** for critical compliance decisions
- **Complex reasoning** over multiple regulations simultaneously
- **Production deployment** with highest quality responses
- **Handling of edge cases** and nuanced regulatory scenarios

For development and testing, consider using `main/` or `interface/` directories for faster iteration.

## Support and Compatibility

Each subdirectory contains platform-specific configurations and dependencies. Refer to individual README files for:
- Detailed setup instructions
- Platform-specific requirements
- Model configuration options
- Performance tuning guidelines
