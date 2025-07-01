# Quick Render Deployment - PharmQAgentAI

## What You Need

### 1. API Keys/Tokens
- **HUGGINGFACE_TOKEN**: Get from https://huggingface.co/settings/tokens
- **GOOGLE_AI_API_KEY**: Get from https://aistudio.google.com/app/apikey (optional)

### 2. Render Account
- Sign up at https://render.com
- Connect your GitHub account

### 3. Your GitHub Repository
- Push this PharmQAgentAI code to GitHub

## Step-by-Step Deployment

### Step 1: Create PostgreSQL Database
1. In Render dashboard → New + → PostgreSQL
2. Name: `pharmqagentai-db`
3. Save the **External Database URL** (starts with postgresql://)

### Step 2: Create Web Service
1. In Render dashboard → New + → Web Service
2. Connect your GitHub repository
3. Configure:
   ```
   Name: pharmqagentai
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
   ```

### Step 3: Add Environment Variables
In your web service settings, add:
```
DATABASE_URL = [your PostgreSQL External URL from Step 1]
HUGGINGFACE_TOKEN = [your Hugging Face token]
GOOGLE_AI_API_KEY = [your Google AI key] (optional)
PORT = 10000
```

### Step 4: Deploy
Click "Deploy" and wait for build to complete.

## Important Notes
- Your app will be at: `https://your-app-name.onrender.com`
- Free tier sleeps after 15 minutes of inactivity
- Database and web service should be in same region
- First deployment takes 5-10 minutes

## If Something Goes Wrong
1. Check build logs in Render dashboard
2. Verify all environment variables are set correctly
3. Ensure DATABASE_URL is the External URL, not Internal
4. Check that your GitHub repo has all the files

That's it! Your PharmQAgentAI will be live on Render with PostgreSQL authentication.