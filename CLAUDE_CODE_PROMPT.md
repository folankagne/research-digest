# Claude Code Debugging Task

## Context
I'm working on a research digest tool that automatically scans academic paper RSS feeds from NBER, ArXiv, CEPR, and other sources, then uses AI to filter and rank them based on my research interests, finally emailing me a personalized weekly digest.

**It was working perfectly for months but broke on January 17, 2026.**

## The Problem

Google deprecated the `google-generativeai` SDK and I've successfully migrated to the new `google-genai` SDK, but I keep getting a 404 error:

```
google.genai.errors.ClientError: 404 NOT_FOUND. 
{'error': {'code': 404, 'message': 'models/gemini-1.5-flash is not found for API version v1, 
or is not supported for generateContent. Call ListModels to see the list of available models 
and their supported methods.', 'status': 'NOT_FOUND'}}
```

**Root Cause:** The model naming convention has changed and I don't know the correct model name to use.

---

## What I Need Help With

### Task 1: List Available Models ⭐ PRIORITY
Write a small Python script that:
1. Uses the new `google-genai` SDK
2. Lists ALL models my API key can access
3. Shows which models support `generateContent` method
4. Displays quota information if available

**Why this is critical:** I've tried multiple model names (`gemini-1.5-flash`, `gemini-pro`, `gemini-2.5-flash`) and all fail with 404. I need to see what's actually available.

### Task 2: Identify the Right Model
Based on the list from Task 1, help me choose a model that:
- ✅ Works with the free tier
- ✅ Has reasonable quota (need at least 10-15 RPM to process papers without failing)
- ✅ Supports long context (I send ~150 paper abstracts in one prompt, roughly 30K-50K tokens)
- ✅ Good for text analysis/filtering tasks

### Task 3: Fix digest.py
Update the `filter_and_rank_papers` function in `digest.py` with:
1. The correct model name
2. Proper API configuration for the new SDK
3. Any additional parameters needed for the new SDK

**Key section to fix** (currently around lines 50-105):
```python
def filter_and_rank_papers(papers, research_interests, max_papers):
    """Use Gemini to filter and rank papers by relevance"""
    from google.genai.types import HttpOptions
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    # THIS IS THE PROBLEM AREA
    client = google.genai.Client(
        api_key=api_key,
        http_options=HttpOptions(api_version="v1")
    )
    
    time.sleep(2)
    
    # ... prompt construction ...
    
    # THIS FAILS WITH 404
    response = client.models.generate_content(
        model='gemini-1.5-flash',  # ❌ WRONG MODEL NAME
        contents=prompt
    )
    
    return response.text
```

### Task 4: Add Error Handling
Add robust error handling for:
- **429 Quota Exhausted:** Retry after delay or fail gracefully
- **404 Model Not Found:** Clear error message, suggest alternatives
- **401/403 Auth Errors:** Check API key validity
- **Rate Limiting:** Add exponential backoff if needed

### Task 5: Test Locally
Run the fixed code locally to verify:
1. API connection works
2. Model responds correctly
3. Response parsing works
4. No quota issues (at least for a small test)

---

## Files to Review

### Primary Files
- **`digest.py`** - Main script (focus on `filter_and_rank_papers` function)
- **`requirements.txt`** - Dependencies (already updated to `google-genai`)
- **`config.yaml`** - Research interests and RSS feeds
- **`TROUBLESHOOTING.md`** - Complete debugging history (READ THIS FIRST!)

### Supporting Files
- **`.github/workflows/digest.yml`** - GitHub Actions workflow (for context)
- **`README.md`** - Original setup instructions

---

## Environment Setup

**Python Version:** 3.10+ (GitHub Actions uses 3.10.20)  
**API Key Location:** Environment variable `GEMINI_API_KEY`  
**Current Directory:** `/home/claude/` or `~/Desktop/research-digest`

**To test locally:**
```bash
# Set your API key
export GEMINI_API_KEY="your-api-key-here"

# Install dependencies
pip install -r requirements.txt

# Run the script
python digest.py
```

**API Key Details:**
- Created: January 17, 2026
- Project: "Default Gemini Project"
- Tier: Free tier
- Location: https://aistudio.google.com/app/apikey

---

## Expected Behavior

When working correctly, the script should:
1. ✅ Fetch ~300 papers from 18 RSS feeds (takes ~10 seconds)
2. ✅ Print: "Analyzing papers with AI..."
3. ✅ Call Gemini API with 150 paper abstracts
4. ✅ Receive ranked list of 12 most relevant papers
5. ✅ Generate HTML email with summaries
6. ✅ Print: "Digest generation complete!"

**Current Behavior:**
```
Fetched 270 papers from 18 sources
Analyzing papers with AI...
[CRASHES with 404 error]
```

---

## Research Context (For Understanding the Use Case)

I'm a PhD student in economics studying:
- Social exclusion and cooperation in prisons (experimental economics)
- Recidivism and rehabilitation policy
- Criminal justice and behavioral economics

The digest filters papers for:
- Experimental/quasi-experimental methods
- Prosocial behavior, cooperation, trust
- Criminal justice policy
- Public goods games, social preferences
- Causal identification (RDD, experiments)

**This context matters because:** The AI needs to understand nuanced academic content and make sophisticated relevance judgments, so I need a capable model (not the most basic one).

---

## Additional Context

### What's Been Tried (All Failed)
See `TROUBLESHOOTING.md` for complete history, but in summary:
- ❌ Tried `gemini-2.5-flash` → quota too low (5 RPM)
- ❌ Tried `gemini-1.5-flash` → 404 error
- ❌ Tried `gemini-pro` → 404 error
- ❌ Tried `gemini-1.5-pro` → 404 error
- ❌ Tried both v1beta and v1 API versions → both fail
- ❌ Tried `gemini-1.5-flash-latest` → 404 error

### SDK Migration Already Complete
The migration from old SDK to new SDK is done:
- ✅ `requirements.txt` updated
- ✅ Imports changed
- ✅ Client initialization rewritten
- ✅ API call syntax updated

**Only remaining issue:** Finding the correct model name.

---

## Success Criteria

The fix is successful when:
1. ✅ Script runs without errors locally
2. ✅ API returns a valid response with paper rankings
3. ✅ Script completes in <60 seconds
4. ✅ No quota errors during normal operation
5. ✅ GitHub Actions workflow passes

---

## Helpful Resources

- **New SDK Docs:** https://googleapis.github.io/python-genai/
- **Migration Guide:** https://github.com/google-gemini/deprecated-generative-ai-python
- **Available Models:** https://ai.google.dev/gemini-api/docs/models/gemini
- **Rate Limits:** https://ai.google.dev/gemini-api/docs/rate-limits

---

## Suggested Workflow

1. **Start by reading `TROUBLESHOOTING.md`** - Understand what's been tried
2. **Write a model listing script** - See what's actually available
3. **Run the listing script** - Get real data from the API
4. **Identify the right model** - Based on quotas and capabilities
5. **Update `digest.py`** - Fix the model name and configuration
6. **Test locally** - Verify it works
7. **Document the fix** - Update TROUBLESHOOTING.md with solution

---

## Questions to Answer

1. What is the correct model name format in the new SDK?
2. Which model has the best balance of capability and quota for free tier?
3. Do we need to change the API version or any other configuration?
4. Should we implement fallback logic in case the model changes again?
5. What's the best way to handle rate limiting for batch processing?

---

## Output Format

Please provide:
1. **Model listing script** with results
2. **Updated `digest.py`** with working model name
3. **Brief explanation** of what was wrong and how you fixed it
4. **Test results** showing it works
5. **Recommendations** for preventing this in the future

---

*Ready to debug! Please start by reading TROUBLESHOOTING.md to understand the full context, then proceed with Task 1.*
