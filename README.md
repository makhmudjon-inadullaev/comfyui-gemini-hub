# ComfyUI-Gemini-Hub

🚀 The ultimate Gemini Hub for ComfyUI - your one-stop destination for all Google AI integrations including Text-to-Speech, Speech-to-Text, Chat, and future Gemini capabilities.

## 🌟 What's in the Hub

- **Text to Speech**: Convert text to speech using Gemini's TTS models with 30+ voice options
- **Speech to Text**: Transcribe audio to text using Gemini's multimodal capabilities  
- **Chat**: Interactive text conversation with Gemini AI models and optional system prompts
- **Growing Collection**: Regular updates with new Gemini APIs and Google AI features
- Seamless ComfyUI workflow integration
- Professional error handling and validation

## 📦 Installation

### Via ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "ComfyUI-Gemini-Hub"
3. Click Install
4. Restart ComfyUI

### Manual Installation
1. Clone this repository to your ComfyUI custom_nodes directory:

   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/makhmudjon-inadullaev/comfyui-gemini-hub.git
   ```

2. Install dependencies:

   ```bash
   cd comfyui-gemini-hub
   pip install -r requirements.txt
   ```

3. Restart ComfyUI

## 🔑 API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Use the API key in the nodes' api_key input field

## Usage

### Text To Speech Node

1. Add the "Gemini Text To Speech" node to your ComfyUI workflow
2. Configure the inputs:
   - **API Key**: Your Gemini API key (get one from Google AI Studio)
   - **Model**: Choose between available Gemini TTS models
   - **Text**: The text you want to convert to speech
   - **Voice Name**: Select from available voices (30+ options available)
3. Connect the audio output to other audio processing nodes or save it directly

### Speech To Text Node

1. Add the "Gemini Speech To Text" node to your ComfyUI workflow
2. Configure the inputs:
   - **API Key**: Your Gemini API key (same as TTS)
   - **Model**: Uses `gemini-2.5-flash-preview-04-17` for transcription
   - **Audio**: Connect an audio input from other nodes or load audio files
### Chat Node

1. Add the "Gemini Chat" node to your ComfyUI workflow
2. Configure the inputs:
   - **API Key**: Your Gemini API key (same as other nodes)
   - **Model**: Uses `gemini-2.5-pro-preview-05-06` for chat
   - **Prompt**: Your message/question to send to Gemini
   - **System Prompt** (Optional): Fine-tune the AI's behavior and personality
3. Connect the text output to other text processing nodes or display it directly

## Input Parameters

### Text To Speech Node

- **api_key** (STRING): Your Gemini API key
- **model** (DROPDOWN): 
  - `gemini-2.5-pro-preview-tts`
  - `gemini-2.5-flash-preview-tts`
- **text** (STRING): Text to be converted to speech
- **voice_name** (DROPDOWN): Voice for speech synthesis
  - `Zephyr`, `Puck`, `Charon`, `Kore`, `Fenrir`, `Leda`
  - `Orus`, `Aoede`, `Callirrhoe`, `Autonoe`, `Enceladus`, `Iapetus`
  - `Umbriel`, `Algieba`, `Despina`, `Erinome`, `Algenib`, `Rasalgethi`
  - `Laomedeia`, `Achernar`, `Alnilam`, `Schedar`, `Gacrux`, `Pulcherrima`
  - `Achird`, `Zubenelgenubi`, `Vindemiatrix`, `Sadachbia`, `Sadaltager`, `Sulafat`

### Speech To Text Node

- **api_key** (STRING): Your Gemini API key
- **model** (DROPDOWN): `gemini-2.5-flash-preview-04-17` (pre-selected)
- **audio** (AUDIO): Audio input to be transcribed to text

### Chat Node

- **api_key** (STRING): Your Gemini API key
- **model** (DROPDOWN): `gemini-2.5-pro-preview-05-06` (pre-selected)
- **prompt** (STRING): Your message/question to send to Gemini
- **system_prompt** (STRING, Optional): System prompt for fine-tuning AI behavior

## Output

### Text To Speech Node
- **audio** (AUDIO): Generated speech audio in ComfyUI's audio format

### Speech To Text Node
- **transcribed_text** (STRING): Transcribed text from the input audio

### Chat Node
- **response** (STRING): Gemini's text response to your prompt

## Requirements

- ComfyUI
- Google Gemini API key
- Internet connection for API calls

## API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Use the API key in the node's api_key input

## Troubleshooting

- Make sure your API key is valid and has access to Gemini TTS models
- Check your internet connection
- Verify that all dependencies are properly installed
- Check ComfyUI console for error messages

## License

This project follows the same license as ComfyUI.
