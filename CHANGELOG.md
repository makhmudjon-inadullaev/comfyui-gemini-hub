# Changelog

All notable changes to ComfyUI-Gemini-Hub will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-31

### Added
- **Initial Gemini Hub Release**: The ultimate hub for all Gemini API integrations
  - Support for `gemini-2.5-pro-preview-tts` and `gemini-2.5-flash-preview-tts` models
  - 30 different voice personalities (Zephyr, Puck, Charon, etc.)
  - Direct ComfyUI audio format output
  - Professional error handling

- **Gemini Speech To Text Node**: Transcribe audio to text
  - Uses `gemini-2.5-flash-preview-04-17` model
  - Support for various audio formats
  - Automatic audio format conversion
  - Clear transcription instructions

- **Gemini Chat Node**: Interactive conversation with AI
  - Uses `gemini-2.5-pro-preview-05-06` model
  - Optional system prompts for behavior customization
  - Streaming response support
  - Business context fine-tuning capability

### Technical Features
- Complete ComfyUI Manager compatibility
- Proper error handling and validation
- Temporary file management
- Base64 audio encoding/decoding
- Cross-platform support (Windows, macOS, Linux)

### Documentation
- Comprehensive README with installation instructions
- API key setup guide
- Usage examples for all nodes
- Troubleshooting section

## [Unreleased]

### Planned for v1.1.0
- **Vision API Integration**: Image analysis and description capabilities
- **Document AI**: PDF and document processing nodes
- **Batch Processing**: Multi-file processing utilities
- **Enhanced Error Messages**: More detailed troubleshooting information

### Planned for v1.2.0  
- **Vertex AI Integration**: Connect to Google Cloud Vertex AI
- **Translation API**: Multi-language translation nodes
- **Search Integration**: Google Search API connectivity
- **Conversation Memory**: Multi-turn conversation support

### Planned for v2.0.0
- **Fine-tuning Integration**: Custom model training utilities  
- **Workflow Templates**: Pre-built business workflow templates
- **Advanced Analytics**: Usage tracking and performance metrics
- **Enterprise Features**: Team collaboration and management tools
