#!/usr/bin/env python3
"""Probe each Gemini model with a real call to find free-tier accessible models."""

import os
import time
import google.genai
import google.genai.errors

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError("Set GEMINI_API_KEY environment variable first")

client = google.genai.Client(api_key=api_key)

SKIP_KEYWORDS = ['tts', 'audio', 'image', 'video', 'veo', 'imagen', 'embed',
                 'aqa', 'robotics', 'computer-use', 'deep-research', 'lyria',
                 'nano-banana', 'live']

print("Probing models with a real API call to find free-tier access...\n")
print(f"{'Model':<50} {'Status'}")
print("-" * 80)

working = []
quota_zero = []
other_errors = []

for model in client.models.list():
    name = model.name
    methods = getattr(model, 'supported_actions', None) or getattr(model, 'supported_generation_methods', [])

    if 'generateContent' not in (methods or []):
        continue

    if any(kw in name.lower() for kw in SKIP_KEYWORDS):
        continue

    try:
        resp = client.models.generate_content(
            model=name,
            contents='Reply with just the word "ok".'
        )
        status = f"OK - response: {resp.text.strip()[:40]!r}"
        working.append(name)
    except google.genai.errors.ClientError as e:
        msg = str(e)
        if '429' in msg:
            if 'limit: 0' in msg or 'RESOURCE_EXHAUSTED' in msg:
                status = "QUOTA ZERO (free tier blocked)"
                quota_zero.append(name)
            else:
                status = "429 Rate limited (has quota but busy)"
                working.append(f"{name} [rate-limited]")
        elif '404' in msg:
            status = "404 Not found"
            other_errors.append(name)
        elif '403' in msg:
            status = "403 Forbidden (paid only?)"
            quota_zero.append(name)
        else:
            status = f"ERROR: {msg[:60]}"
            other_errors.append(name)
    except Exception as e:
        status = f"UNEXPECTED: {str(e)[:60]}"
        other_errors.append(name)

    print(f"{name:<50} {status}")
    time.sleep(0.5)  # avoid hammering

print("\n" + "=" * 80)
print(f"\n✅ WORKING (free tier accessible): {len(working)}")
for m in working:
    print(f"   {m}")

print(f"\n❌ QUOTA ZERO / BLOCKED: {len(quota_zero)}")
for m in quota_zero:
    print(f"   {m}")

print(f"\n⚠️  OTHER ERRORS: {len(other_errors)}")
for m in other_errors:
    print(f"   {m}")
