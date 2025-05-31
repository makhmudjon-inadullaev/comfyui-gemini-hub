import base64
import tempfile
import os
from google import genai
from google.genai import types
import folder_paths
import torch
import torchaudio


class GeminiSpeechToText:
    """
    A ComfyUI node for converting speech to text using Google's Gemini API
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "tooltip": "Your Gemini API key"
                }),
                "model": (["gemini-2.5-flash-preview-04-17"], {
                    "default": "gemini-2.5-flash-preview-04-17",
                    "tooltip": "Gemini model to use for speech-to-text transcription"
                }),
                "audio": ("AUDIO", {
                    "tooltip": "Audio input to be transcribed to text"
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("transcribed_text",)
    FUNCTION = "transcribe_audio"
    CATEGORY = "audio"
    
    def audio_to_base64(self, audio_dict, format="wav"):
        """Convert ComfyUI audio format to base64 string"""
        try:
            # Extract waveform and sample rate from audio dict
            if isinstance(audio_dict, dict):
                waveform = audio_dict.get("waveform")
                sample_rate = audio_dict.get("sample_rate", 44100)
            else:
                # Fallback if audio is passed as tensor directly
                waveform = audio_dict
                sample_rate = 44100
            
            # Remove batch dimension if present
            if waveform.dim() > 2:
                waveform = waveform.squeeze(0)
            
            # Create temporary file
            temp_dir = folder_paths.get_temp_directory()
            temp_file = tempfile.NamedTemporaryFile(
                suffix=f".{format}", 
                dir=temp_dir, 
                delete=False
            )
            
            # Save audio to temporary file
            torchaudio.save(temp_file.name, waveform, sample_rate, format=format.upper())
            temp_file.close()
            
            # Read file and convert to base64
            with open(temp_file.name, 'rb') as f:
                audio_bytes = f.read()
            
            # Clean up temporary file
            os.unlink(temp_file.name)
            
            # Convert to base64
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
            mime_type = f"audio/{format}"
            
            return base64_audio, mime_type
            
        except Exception as e:
            raise ValueError(f"Error converting audio to base64: {str(e)}")
    
    def transcribe_audio(self, api_key, model, audio):
        """Transcribe audio to text using Gemini API"""
        try:
            # Initialize the Gemini client
            client = genai.Client(api_key=api_key)
            
            # Convert audio to base64
            base64_audio, mime_type = self.audio_to_base64(audio)
            
            # Prepare the audio part for the API using inline_data
            audio_part = types.Part(
                inline_data=types.Blob(
                    mime_type=mime_type,
                    data=base64_audio
                )
            )
            
            # Prepare the text instruction part
            text_part = types.Part.from_text(
                text="Transcribe the following audio. Provide only the transcribed text output, without any additional commentary or conversational filler. If the audio is unclear or contains no speech, indicate that appropriately."
            )
            
            # Prepare the content for the API
            contents = [
                types.Content(
                    role="user",
                    parts=[audio_part, text_part],
                ),
            ]
            
            # Generate the transcription
            response = client.models.generate_content(
                model=model,
                contents=contents,
            )
            
            # Extract transcribed text
            if response.text is None or response.text == "":
                raise ValueError("Received no valid text in the transcript from Gemini API")
            
            transcribed_text = response.text.strip()
            
            return (transcribed_text,)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error transcribing audio: {error_msg}")
            
            # Handle specific error cases
            if "API key not valid" in error_msg:
                raise ValueError("Invalid API Key. Please check your API key.")
            elif "Unsupported content type" in error_msg or "audio format" in error_msg.lower():
                raise ValueError(f"The audio format may not be supported by the Gemini model for transcription. Details: {error_msg}")
            else:
                raise ValueError(f"Gemini API transcription request failed: {error_msg}")


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "GeminiSpeechToText": GeminiSpeechToText
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiSpeechToText": "Gemini Speech To Text"
}
