# How to Get IBM watsonx.ai Project ID and Space ID

## Step-by-Step Guide

### Option 1: Using Project ID (Recommended for Development)

1. **Go to IBM watsonx.ai**
   - Visit: https://dataplatform.cloud.ibm.com/wx/home
   - Or go to: https://cloud.ibm.com/ → Search for "watsonx.ai"

2. **Open or Create a Project**
   - Click on "Projects" in the left sidebar
   - Either open an existing project or click "New project"
   - If creating new: Give it a name like "ProcessDoctor" and click "Create"

3. **Get the Project ID**
   - Once in your project, click on the **"Manage"** tab at the top
   - Click on **"General"** in the left sidebar
   - You'll see **"Project ID"** - this is a long string like: `12345678-1234-1234-1234-123456789abc`
   - Copy this entire ID

4. **Update your .env file**
   ```bash
   GRANITE_PROJECT_ID=12345678-1234-1234-1234-123456789abc
   BOB_PROJECT_ID=12345678-1234-1234-1234-123456789abc
   ```

### Option 2: Using Space ID (For Production Deployments)

1. **Go to IBM watsonx.ai**
   - Visit: https://dataplatform.cloud.ibm.com/wx/home

2. **Create a Deployment Space**
   - Click on **"Deployments"** in the left sidebar
   - Click **"New deployment space"**
   - Give it a name like "ProcessDoctor Production"
   - Select your machine learning service
   - Click "Create"

3. **Get the Space ID**
   - Open your deployment space
   - Click on the **"Manage"** tab
   - You'll see **"Space GUID"** or **"Space ID"**
   - Copy this ID

4. **Update your .env file**
   ```bash
   GRANITE_SPACE_ID=your-space-id-here
   BOB_SPACE_ID=your-space-id-here
   ```

### Which Should You Use?

**Use Project ID if:**
- You're in development/testing
- You want to experiment with models
- You're building and testing prompts

**Use Space ID if:**
- You're deploying to production
- You have deployed model instances
- You need consistent model endpoints

**For this hackathon, use PROJECT ID** - it's simpler and works for development.

## Complete .env Configuration Example

```bash
# IBM watsonx.ai Configuration
GRANITE_API_KEY=your_api_key_from_ibm_cloud
GRANITE_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1
GRANITE_MODEL=ibm/granite-13b-chat-v2
GRANITE_PROJECT_ID=12345678-1234-1234-1234-123456789abc
GRANITE_SPACE_ID=

# Bob uses same credentials
BOB_API_KEY=your_api_key_from_ibm_cloud
BOB_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1
BOB_PROJECT_ID=12345678-1234-1234-1234-123456789abc
BOB_SPACE_ID=

# Set to false to use real API
USE_MOCK_MODE=false
```

## How to Get Your API Key

1. Go to: https://cloud.ibm.com/iam/apikeys
2. Click **"Create"**
3. Give it a name like "watsonx-processdoctor"
4. Click **"Create"**
5. **Copy the API key immediately** (you can't see it again!)
6. Paste it in your `.env` file

## Verify Your Region

Make sure your API URL matches your IBM Cloud region:

- **US South**: `https://us-south.ml.cloud.ibm.com/ml/v1`
- **US East**: `https://us-east.ml.cloud.ibm.com/ml/v1`
- **EU Germany**: `https://eu-de.ml.cloud.ibm.com/ml/v1`
- **EU UK**: `https://eu-gb.ml.cloud.ibm.com/ml/v1`
- **Japan**: `https://jp-tok.ml.cloud.ibm.com/ml/v1`

Check your region in IBM Cloud console and update the URL accordingly.

## Testing Your Configuration

After updating your `.env` file:

1. **Restart your backend server**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. **Test in the frontend**:
   - Enter a workflow description
   - Click "Diagnose workflow"
   - If configured correctly, you'll see real AI analysis!

## Troubleshooting

### Still getting 401 errors?
- Double-check your API key is correct (no extra spaces)
- Verify the Project ID is from the same IBM Cloud account
- Make sure your API key has access to watsonx.ai service

### Can't find Project ID?
- Make sure you're in a **watsonx.ai project**, not just any IBM Cloud project
- Look under: Project → Manage → General → Project ID

### Wrong region?
- Check your IBM Cloud region in the top-right corner
- Update `GRANITE_API_URL` to match your region

## Quick Summary

**You need 3 things:**
1. ✅ API Key (from IBM Cloud IAM)
2. ✅ Project ID (from watsonx.ai project)
3. ✅ Correct API URL (matching your region)

Once you have all three, update your `.env` file and restart the server!