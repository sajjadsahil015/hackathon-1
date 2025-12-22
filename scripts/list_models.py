#!/usr/bin/env python3
"""List available Gemini models."""
from pathlib import Path
from dotenv import dotenv_values

# Load from .env
env_path = Path(__file__).parent.parent / ".env"
config = dotenv_values(env_path)
api_key = config.get("GOOGLE_API_KEY", "")

import google.generativeai as genai
genai.configure(api_key=api_key)

print("Available models for generateContent:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")
