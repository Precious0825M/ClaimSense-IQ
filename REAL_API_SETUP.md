# Real API Integration Setup

To use real AI models instead of mock data, you need to configure API keys for IBM's AI services.

## Required API Keys

### 1. IBM watsonx (for Granite models)
- **What it does**: Powers the AI analysis and optimization
- **How to get it**:
  1. Go to [IBM Cloud](https://cloud.ibm.com/)
  2. Create a watsonx.ai instance
  3. Get your API key from the service credentials
  4. Get your project ID

### 2. OpenAI API (Alternative)
If you don't have IBM watsonx access, you can use OpenAI:
- **How to get it**:
  1. Go to [OpenAI Platform](https://platform.openai.com/)
  2. Create an account
  3. Generate an API key

### 3. GitHub Token (Optional but recommended)
- **What it does**: Allows fetching workflows from private repos and creating PRs
- **How to get it**:
  1. Go to GitHub Settings → Developer settings → Personal access tokens
  2. Generate new token with `repo` and `workflow` scopes

## Configuration

### Option 1: Use IBM watsonx (Recommended)

Edit `backend/.env`:
```bash
# Disable mock mode
USE_MOCK_MODE=false

# IBM watsonx credentials
GRANITE_API_KEY=your_watsonx_api_key_here
GRANITE_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1
GRANITE_MODEL=ibm/granite-13b-chat-v2

# Same for Bob (or use same watsonx credentials)
BOB_API_KEY=your_watsonx_api_key_here
BOB_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1

# GitHub token for repo access
GITHUB_TOKEN=ghp_your_github_token_here
```

### Option 2: Use OpenAI (Easier to get started)

You'll need to modify the LLM client to support OpenAI. Edit `backend/.env`:
```bash
# Disable mock mode
USE_MOCK_MODE=false

# OpenAI API
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_MODEL=gpt-4

# GitHub token
GITHUB_TOKEN=ghp_your_github_token_here
```

Then update `backend/app/agents/llm_client.py` to add OpenAI support.

## Quick Start with OpenAI

Since OpenAI is easier to access, here's how to set it up:

1. **Get OpenAI API Key**:
   ```bash
   # Visit https://platform.openai.com/api-keys
   # Create new key and copy it
   ```

2. **Update backend/.env**:
   ```bash
   USE_MOCK_MODE=false
   OPENAI_API_KEY=sk-your-key-here
   ```

3. **Install OpenAI SDK**:
   ```bash
   cd backend
   pip install openai
   ```

4. **I can update the code to use OpenAI** - just let me know!

## Current Status

Right now, the system is in **mock mode** because:
- No API keys are configured
- This prevents errors when IBM services aren't available
- Mock data is returned for all AI operations

## What Happens When You Disable Mock Mode

With `USE_MOCK_MODE=false` and proper API keys:

1. **Text Input**: AI analyzes your workflow description
2. **GitHub URL**: System fetches actual workflows from the repo
3. **Real Analysis**: AI identifies actual bottlenecks
4. **Real Optimization**: AI generates actual optimized workflows
5. **PR Creation**: Creates real pull requests (with GitHub token)

## Cost Considerations

- **IBM watsonx**: Pay per token, varies by model
- **OpenAI GPT-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **OpenAI GPT-3.5**: Much cheaper, ~$0.001 per 1K tokens

## Next Steps

**Choose your path:**

1. **I have IBM watsonx access** → Provide API keys, I'll help configure
2. **I want to use OpenAI** → Get API key, I'll update the code
3. **I want to test with mock data first** → Keep `USE_MOCK_MODE=true`

Let me know which option you prefer and I'll help you set it up!