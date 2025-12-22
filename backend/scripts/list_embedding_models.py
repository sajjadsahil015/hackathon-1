#!/usr/bin/env python3
"""List available Gemini embedding models."""
from pathlib import Path
from dotenv import dotenv_values

env_path = Path(__file__).parent.parent / ".env"
config = dotenv_values(env_path)
api_key = config.get("GOOGLE_API_KEY", "")

import google.generativeai as genai
genai.configure(api_key=api_key)

print("Available embedding models:")
for model in genai.list_models():
    if 'embedContent' in model.supported_generation_methods:
        print(f"  - {model.name} (dimension: {getattr(model, 'output_token_limit', 'N/A')})")
