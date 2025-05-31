import base64
import mimetypes
import os
import re
import struct
import tempfile
from google import genai
from google.genai import types
import folder_paths
import torch
import torchaudio


class GeminiTextToSpeech:
    """
    A ComfyUI node for converting text to speech using Google's Gemini API
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
                "model": (["gemini-2.5-pro-preview-tts", "gemini-2.5-flash-preview-tts"], {
                    "default": "gemini-2.5-flash-preview-tts",
                    "tooltip": "Select the Gemini model to use for text-to-speech"
                }),
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, this is a test of Gemini text to speech.",
                    "tooltip": "Text to be converted to speech"
                }),
                "voice_name": ([
                    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", 
                    "Orus", "Aoede", "Callirrhoe", "Autonoe", "Enceladus", "Iapetus",
                    "Umbriel", "Algieba", "Despina", "Erinome", "Algenib", "Rasalgethi",
                    "Laomedeia", "Achernar", "Alnilam", "Schedar", "Gacrux", "Pulcherrima",
                    "Achird", "Zubenelgenubi", "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat"
                ], {
                    "default": "Zephyr",
                    "tooltip": "Voice to use for speech synthesis"
                })
            }
        }
    
    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "generate_speech"
    CATEGORY = "audio"
    
    def save_binary_file(self, file_name, data):
        """Save binary data to file"""
        with open(file_name, "wb") as f:
            f.write(data)
        return file_name
    
    def convert_to_wav(self, audio_data: bytes, mime_type: str) -> bytes:
        """Generates a WAV file header for the given audio data and parameters."""
        parameters = self.parse_audio_mime_type(mime_type)
        bits_per_sample = parameters["bits_per_sample"]
        sample_rate = parameters["rate"]
        num_channels = 1
        data_size = len(audio_data)
        bytes_per_sample = bits_per_sample // 8
        block_align = num_channels * bytes_per_sample
        byte_rate = sample_rate * block_align
        chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

        # http://soundfile.sapp.org/doc/WaveFormat/
        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",          # ChunkID
            chunk_size,       # ChunkSize (total file size - 8 bytes)
            b"WAVE",          # Format
            b"fmt ",          # Subchunk1ID
            16,               # Subchunk1Size (16 for PCM)
            1,                # AudioFormat (1 for PCM)
            num_channels,     # NumChannels
            sample_rate,      # SampleRate
            byte_rate,        # ByteRate
            block_align,      # BlockAlign
            bits_per_sample,  # BitsPerSample
            b"data",          # Subchunk2ID
            data_size         # Subchunk2Size (size of audio data)
        )
        return header + audio_data

    def parse_audio_mime_type(self, mime_type: str) -> dict[str, int]:
        """Parses bits per sample and rate from an audio MIME type string."""
        bits_per_sample = 16
        rate = 24000

        # Extract rate from parameters
        parts = mime_type.split(";")
        for param in parts:
            param = param.strip()
            if param.lower().startswith("rate="):
                try:
                    rate_str = param.split("=", 1)[1]
                    rate = int(rate_str)
                except (ValueError, IndexError):
                    pass  # Keep rate as default
            elif param.startswith("audio/L"):
                try:
                    bits_per_sample = int(param.split("L", 1)[1])
                except (ValueError, IndexError):
                    pass  # Keep bits_per_sample as default

        return {"bits_per_sample": bits_per_sample, "rate": rate}
    
    def generate_speech(self, api_key, model, text, voice_name):
        """Generate speech from text using Gemini API"""
        try:
            # Initialize the Gemini client
            client = genai.Client(api_key=api_key)
            
            # Prepare the content for the API
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=text),
                    ],
                ),
            ]
            
            # Configure the generation settings
            generate_content_config = types.GenerateContentConfig(
                temperature=1,
                response_modalities=["audio"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
            )
            
            # Generate the audio content
            audio_data = b""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                
                if (chunk.candidates[0].content.parts[0].inline_data and 
                    chunk.candidates[0].content.parts[0].inline_data.data):
                    inline_data = chunk.candidates[0].content.parts[0].inline_data
                    data_buffer = inline_data.data
                    
                    # Convert to WAV if necessary
                    file_extension = mimetypes.guess_extension(inline_data.mime_type)
                    if file_extension is None or file_extension != ".wav":
                        data_buffer = self.convert_to_wav(inline_data.data, inline_data.mime_type)
                    
                    audio_data += data_buffer
            
            if not audio_data:
                raise ValueError("No audio data received from Gemini API")
            
            # Save to temporary file
            temp_dir = folder_paths.get_temp_directory()
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".wav", 
                dir=temp_dir, 
                delete=False
            )
            temp_file.write(audio_data)
            temp_file.close()
            
            # Load the audio file using torchaudio
            waveform, sample_rate = torchaudio.load(temp_file.name)
            
            # Clean up the temporary file
            os.unlink(temp_file.name)
            
            # Return the audio in ComfyUI's expected format
            audio_dict = {
                "waveform": waveform.unsqueeze(0),  # Add batch dimension
                "sample_rate": sample_rate
            }
            
            return (audio_dict,)
            
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            raise e


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "GeminiTextToSpeech": GeminiTextToSpeech
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiTextToSpeech": "Gemini Text To Speech"
}
