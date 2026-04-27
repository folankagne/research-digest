# Research Digest Troubleshooting Log

## Problem Summary
The research digest stopped working on January 17, 2026 due to Google deprecating the `google-generativeai` SDK and changing model names/quotas.

## Timeline of Issues

### Issue 1: Quota Exhaustion (Initial)
**Error:** `429 You exceeded your current quota... gemini-2.5-flash... limit: 5`

**What happened:** Google reduced free tier quotas in December 2025. The `gemini-2.5-flash` model went from 15 RPM to only 5 RPM, causing immediate quota exhaustion when processing 300 papers.

**Attempted fix:** Try switching to `gemini-1.5-flash` (15 RPM)  
**Result:** Failed - model name not recognized by the deprecated SDK

---

### Issue 2: Deprecated SDK
**Error:** 
```
FutureWarning: All support for the `google.generativeai` package has ended.
Please switch to the `google.genai` package as soon as possible.
```

**What happened:** Google completely deprecated the old `google-generativeai` SDK. The v1beta API no longer recognizes model names that worked before.

**Fix applied:** Migrated from `google-generativeai` to `google-genai`

**Changes made:**
- `requirements.txt`: Changed `google-generativeai` → `google-genai`
- `digest.py` line 10: Changed `import google.generativeai as genai` → `import google.genai`
- `digest.py`: Rewrote API client initialization and calls to use new SDK syntax

---

### Issue 3: Model Name Not Found (v1beta API)
**Error:** `404 NOT_FOUND. models/gemini-1.5-flash is not found for API version v1beta`

**What happened:** New SDK defaults to `v1beta` API version which doesn't recognize the `gemini-1.5-flash` model name.

**Attempted fix:** Explicitly specify API version `v1` instead of `v1beta`  
**Result:** Still failing with same 404 error

---

### Issue 4: Model Name Not Found (v1 API)
**Error:** 
```
google.genai.errors.ClientError: 404 NOT_FOUND. 
{'error': {'code': 404, 'message': 'models/gemini-1.5-flash is not found for API version v1, 
or is not supported for generateContent. Call ListModels to see the list of available models 
and their supported methods.', 'status': 'NOT_FOUND'}}
```

**What happened:** Even with v1 API specified, the model name format has changed and we don't know the correct naming convention.

**Attempted fix:** Tried various model name formats  
**Result:** All attempts failed

---

## Current Status: BLOCKED

**Current error:**
```
google.genai.errors.ClientError: 404 NOT_FOUND. 
{'error': {'code': 404, 'message': 'models/gemini-1.5-flash is not found for API version v1'}}
```

**Root cause:** The model naming convention has changed in the new SDK and we need to discover the correct format.

**Tried model names (all failed with 404):**
- `gemini-2.5-flash` ❌ (would have quota issues anyway - only 5 RPM)
- `gemini-1.5-flash` ❌ 
- `gemini-pro` ❌
- `gemini-1.5-pro` ❌
- `gemini-1.5-flash-latest` ❌
- `gemini-1.0-pro` ❌

**Next steps needed:**
1. List available models using the new SDK's API
2. Find the correct model name format for text generation
3. Verify the model has adequate free tier quotas (need 15+ RPM)
4. Update code with working model name
5. Test end-to-end

---

## Code Changes Made

### File: `requirements.txt`
**Before:**
```
feedparser
PyYAML
google-generativeai
```

**After:**
```
feedparser
PyYAML
google-genai
```

### File: `digest.py`

**Import changes (line 10):**
```python
# Before:
import google.generativeai as genai

# After:
import google.genai
from google.genai.types import HttpOptions
```

**Client initialization (lines ~50-58):**
```python
# Before (old SDK):
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# After (new SDK):
from google.genai.types import HttpOptions

client = google.genai.Client(
    api_key=api_key,
    http_options=HttpOptions(api_version="v1")
)
```

**API call (lines ~100-105):**
```python
# Before (old SDK):
response = model.generate_content(prompt)
return response.text

# After (new SDK):
response = client.models.generate_content(
    model='gemini-1.5-flash',  # ❌ THIS MODEL NAME DOESN'T WORK
    contents=prompt
)
return response.text
```

---

## What Needs to Be Fixed

### Priority 1: Find Working Model
1. **List available models** - Use new SDK to enumerate models accessible with our API key
2. **Identify correct model name** - Find the right format for v1 API
3. **Check quotas** - Verify chosen model has adequate free tier (15+ RPM preferred)

### Priority 2: Update Code
4. **Update model name** in `digest.py` with working value
5. **Test locally** before pushing to GitHub Actions

### Priority 3: Add Robustness
6. **Error handling** for quota exhaustion (429 errors)
7. **Rate limiting** to avoid hitting RPM limits (currently processing 150 papers in one call)
8. **Fallback model** in case primary model is unavailable
9. **Better logging** to debug future issues

---

## Working Configuration (Last Known Good - Before Jan 17, 2026)

**SDK:** `google-generativeai` (deprecated)  
**Model:** `gemini-2.5-flash`  
**Quota:** 10-15 RPM (was reduced to 5 RPM in late Dec 2025)  
**API Version:** v1beta (implicit)  

This configuration worked reliably for several months until Google's SDK deprecation.

---

## Key Learnings

1. **Google silently reduced quotas** in December 2025 without advance notice to free tier users
2. **Model names changed** between SDK versions - what worked in old SDK doesn't work in new SDK
3. **API version matters** - v1beta vs v1 have different model availability
4. **Documentation lags** - official docs don't always reflect current model names
5. **Free tier is unstable** - Google can change limits/access without warning

---

## Resources

- **New SDK Documentation:** https://googleapis.github.io/python-genai/
- **Migration Guide:** https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md
- **Rate Limits Page:** https://ai.google.dev/gemini-api/docs/rate-limits
- **API Key Management:** https://aistudio.google.com/app/apikey
- **Model Pricing:** https://ai.google.dev/gemini-api/docs/pricing
- **PyPI Package:** https://pypi.org/project/google-genai/

---

## Environment Details

**Runtime:** GitHub Actions (Ubuntu 24.04)  
**Python Version:** 3.10.20  
**Installed Packages:**
- `google-genai` (latest)
- `feedparser`
- `PyYAML`

**API Key:** Stored in GitHub Secrets as `GEMINI_API_KEY`  
**Created:** January 17, 2026  
**Project:** Default Gemini Project (gen-lang-client-0705034890)  
**Tier:** Free tier ("Niveau sans frais")

---

## Questions for Debugging

1. How do we list available models using the new `google-genai` SDK?
2. What is the correct model name format for the v1 API in 2026?
3. How do we programmatically check our API key's quota and permissions?
4. Should we implement automatic model fallback if primary model is unavailable?
5. Is there a way to test model availability without consuming quota?
6. What's the best practice for handling rate limits when processing large batches?

---

## Contact Points

**Original Tool Creator:** zytynski (GitHub)  
**Repository:** https://github.com/folankagne/research-digest (fork)  
**Upstream:** https://github.com/zytynski/research-digest (original)

---

*Last Updated: January 17, 2026*
