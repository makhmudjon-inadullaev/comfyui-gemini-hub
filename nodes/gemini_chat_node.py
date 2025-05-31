import os
from google import genai
from google.genai import types


class GeminiChat:
    """
    A ComfyUI node for chatting with Google's Gemini API
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
                "model": (["gemini-2.5-pro-preview-05-06"], {
                    "default": "gemini-2.5-pro-preview-05-06",
                    "tooltip": "Gemini model to use for chat"
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Hello, how are you?",
                    "tooltip": "Your message/prompt to send to Gemini"
                })
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Optional system prompt for fine-tuning the AI's behavior"
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "chat_with_gemini"
    CATEGORY = "text"
    
    def chat_with_gemini(self, api_key, model, prompt, system_prompt=""):
        """Chat with Gemini API and get text response"""
        try:
            # Initialize the Gemini client
            client = genai.Client(api_key=api_key)
            
            # Prepare the user message, incorporating system prompt if provided
            user_message = prompt
            if system_prompt and system_prompt.strip():
                user_message = f"{system_prompt.strip()}\n\nUser: {prompt}"
            
            # Prepare the contents list
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=user_message),
                    ],
                )
            ]
            
            # Configure the generation settings
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
            )
            
            # Generate the response
            response_text = ""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    response_text += chunk.text
            
            if not response_text:
                raise ValueError("Received empty response from Gemini API")
            
            return (response_text.strip(),)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error chatting with Gemini: {error_msg}")
            
            # Handle specific error cases
            if "API key not valid" in error_msg:
                raise ValueError("Invalid API Key. Please check your API key.")
            elif "model not found" in error_msg.lower():
                raise ValueError(f"The model '{model}' may not be available. Please check the model name.")
            else:
                raise ValueError(f"Gemini API chat request failed: {error_msg}")


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "GeminiChat": GeminiChat
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiChat": "Gemini Chat"
}
