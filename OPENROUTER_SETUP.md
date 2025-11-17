# OpenRouter Integration Guide

SmartResume AI now supports **two AI providers**:

1. **Google Gemini** (Primary, recommended)
2. **OpenRouter** (Alternative, includes free models)

## Why OpenRouter?

- **Free Models Available**: Access to Google Gemma and other free models
- **No Credit Card Required**: Get started immediately
- **Fallback Option**: Works if Gemini quota is exceeded
- **Multiple Models**: Switch between different AI models

## Setup Instructions

### Step 1: Get OpenRouter API Key

1. Visit https://openrouter.ai/keys
2. Sign up or log in
3. Click "Create Key"
4. Copy your API key

### Step 2: Configure .env File

Add these lines to your `.env` file:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_SITE_URL=http://localhost:8503
OPENROUTER_SITE_NAME=SmartResume AI
```

### Step 3: Choose Your Model

Edit `utils/openrouter_client.py` and change the model:

```python
# Free models available:
self.model = "google/gemma-2-9b-it:free"          # Fast, free (recommended)
# self.model = "meta-llama/llama-3.2-3b-instruct:free"  # Alternative free model
# self.model = "nousresearch/hermes-3-llama-3.1-405b:free"  # Larger free model

# Paid models (better quality):
# self.model = "google/gemini-pro"
# self.model = "anthropic/claude-3.5-sonnet"
# self.model = "openai/gpt-4-turbo"
```

## How It Works

The app automatically:
1. Tries to use **Gemini** first (if API key exists)
2. Falls back to **OpenRouter** if Gemini fails
3. Shows which provider is active in the UI

## Free Model Limits

OpenRouter free models have limits:
- **Gemma 2 9B**: Unlimited requests, rate limited
- **Llama 3.2**: Unlimited requests, rate limited
- No credit card required

## Request Format

The OpenRouter client uses the same interface as Gemini:

```python
from utils.ai_client import AIClient

client = AIClient()  # Automatically picks Gemini or OpenRouter
response = client.generate_content("Write a professional summary...")
```

## Supported Features

All SmartResume AI features work with OpenRouter:
- ✅ Professional Summary Generation
- ✅ Experience Bullet Points
- ✅ Project Descriptions
- ✅ Skills Suggestions
- ✅ Cover Letter Generation
- ✅ Resume Quality Analysis

## Troubleshooting

**Error: "No AI API keys found"**
- Add either `GEMINI_API_KEY` or `OPENROUTER_API_KEY` to `.env`

**Error: "Rate limit exceeded"**
- Wait a few seconds and try again
- Free models have rate limits

**Error: "Invalid API key"**
- Check your API key is correct in `.env`
- Make sure you copied the full key

## Cost Comparison

| Provider | Model | Cost | Speed | Quality |
|----------|-------|------|-------|---------|
| Gemini | gemini-2.5-flash | Free* | Fast | Excellent |
| OpenRouter | gemma-2-9b-it:free | Free | Fast | Good |
| OpenRouter | llama-3.2-3b:free | Free | Fast | Good |
| OpenRouter | gemini-pro | Paid | Fast | Excellent |

*Gemini has free tier with daily limits

## Recommended Setup

For best experience:
1. Use **Gemini** as primary (faster, better quality)
2. Add **OpenRouter** as backup (free, no quota issues)
3. Configure both API keys in `.env`

The app will automatically use the best available option!
