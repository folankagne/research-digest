#!/usr/bin/env python3
"""List all Gemini models available for this API key."""

import os
import google.genai

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError("Set GEMINI_API_KEY environment variable first")

client = google.genai.Client(api_key=api_key)

print(f"{'Model Name':<45} {'Supported Methods'}")
print("-" * 80)

generate_content_models = []
for model in client.models.list():
    methods = getattr(model, 'supported_actions', None) or getattr(model, 'supported_generation_methods', [])
    methods_str = ', '.join(methods) if methods else 'unknown'
    print(f"{model.name:<45} {methods_str}")
    if 'generateContent' in (methods or []):
        generate_content_models.append(model.name)

print("\n=== Models supporting generateContent ===")
for m in generate_content_models:
    print(f"  {m}")
