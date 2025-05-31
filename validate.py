#!/usr/bin/env python3
"""
ComfyUI-Gemini-Hub Validation Script
This script validates that all nodes can be imported correctly
"""

import sys
import os

def validate_nodes():
    """Validate that all nodes can be imported"""
    print("🔍 ComfyUI-Gemini-Hub Node Validation")
    print("=====================================")
    
    try:
        # Test TTS Node
        print("📢 Testing Text-to-Speech Node...")
        from nodes.gemini_text_to_speech_node import GeminiTextToSpeechNode
        print("✅ TTS Node imported successfully")
        
        # Test STT Node  
        print("🎤 Testing Speech-to-Text Node...")
        from nodes.gemini_speech_to_text_node import GeminiSpeechToTextNode
        print("✅ STT Node imported successfully")
        
        # Test Chat Node
        print("💬 Testing Chat Node...")
        from nodes.gemini_chat_node import GeminiChatNode
        print("✅ Chat Node imported successfully")
        
        # Test main module
        print("📦 Testing main module...")
        import __init__
        print(f"✅ Main module imported with {len(__init__.NODE_CLASS_MAPPINGS)} nodes")
        
        print("\n🎉 All nodes validated successfully!")
        print("📋 Available nodes:")
        for node_name in __init__.NODE_CLASS_MAPPINGS.keys():
            print(f"   - {node_name}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n🔧 Checking Dependencies")
    print("========================")
    
    required_packages = ['google.genai', 'torch', 'torchaudio']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'google.genai':
                import google.genai
            elif package == 'torch':
                import torch
            elif package == 'torchaudio':
                import torchaudio
            print(f"✅ {package} - Available")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies satisfied")
        return True

if __name__ == "__main__":
    print("Starting ComfyUI-Gemini-Hub validation...\n")
    
    deps_ok = check_dependencies()
    nodes_ok = validate_nodes()
    
    if deps_ok and nodes_ok:
        print("\n🎊 ComfyUI-Gemini-Hub is ready for deployment!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed. Please fix the issues above.")
        sys.exit(1)
