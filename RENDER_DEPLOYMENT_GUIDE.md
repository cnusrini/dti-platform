# PharmQAgentAI Render Deployment Guide

## Overview
This guide will help you deploy PharmQAgentAI to Render with PostgreSQL database integration.

## Prerequisites

### 1. GitHub Repository
- Push your PharmQAgentAI code to a GitHub repository
- Ensure all files are committed and pushed

### 2. Render Account
- Create a free account at [render.com](https://render.com)
- Connect your GitHub account to Render

## Deployment Steps

### Step 1: Create PostgreSQL Database on Render

1. **Log into Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" button
   - Select "PostgreSQL"

2. **Configure Database**
   - **Name**: `pharmqagentai-db`
   - **Database**: `pharmqagentai`
   - **User**: `pharmqagentai_user`
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 15 (recommended)
   - **Plan**: Free (for testing) or Starter+ (for production)

3. **Save Database Credentials**
   After creation, you'll get:
   - **Database URL**: `postgresql://username:password@hostname:port/database`
   - **Internal Database URL**: For internal connections
   - **External Database URL**: For external connections

### Step 2: Create Web Service on Render

1. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

2. **Configure Web Service**
   ```
   Name: pharmqagentai
   Environment: Python 3
   Region: Same as your database
   Branch: main (or your main branch)
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
   ```

3. **Environment Variables**
   Add these environment variables in Render:
   ```
   DATABASE_URL=<your-render-postgresql-url>
   HUGGINGFACE_TOKEN=<your-huggingface-token>
   GOOGLE_AI_API_KEY=<your-google-ai-key>
   PORT=10000
   ```

### Step 3: Required Files for Deployment

#### requirements.txt
```
streamlit>=1.45.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
torch>=2.1.0
transformers>=4.36.0
psycopg2-binary>=2.9.7
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
anthropic>=0.7.0
```

#### runtime.txt
```
python-3.11.6
```

#### .streamlit/config.toml
```toml
[server]
headless = true
address = "0.0.0.0"
port = 10000
maxUploadSize = 200

[theme]
base = "light"
```

## Environment Variables You Need

### 1. DATABASE_URL
```
postgresql://username:password@hostname:port/database
```
- Get this from your Render PostgreSQL database
- Copy the "External Database URL"

### 2. HUGGINGFACE_TOKEN
```
hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Get from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Create a new token with "Read" access

### 3. GOOGLE_AI_API_KEY (Optional)
```
AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Enables advanced AI agent features

## Deployment Process

### 1. Prepare Your Repository
```bash
# Ensure all files are in your repository
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Database Setup
1. Create PostgreSQL database on Render
2. Copy the External Database URL
3. Test connection (optional)

### 3. Web Service Setup
1. Create web service connected to your GitHub repo
2. Add all environment variables
3. Set build and start commands
4. Deploy

### 4. Verify Deployment
1. Check build logs for errors
2. Verify database connection
3. Test login functionality
4. Test core features

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
- Verify DATABASE_URL is correct
- Ensure database is in same region as web service
- Check database credentials

#### 2. Build Failures
- Verify requirements.txt has all dependencies
- Check Python version compatibility
- Review build logs for specific errors

#### 3. Port Issues
- Ensure PORT environment variable is set
- Use $PORT in start command
- Verify Streamlit config uses correct port

#### 4. Memory Issues
- Consider upgrading to paid plan for more resources
- Optimize model loading in application
- Use model caching strategically

## Post-Deployment Steps

### 1. Custom Domain (Optional)
- Add custom domain in Render dashboard
- Update DNS records
- Configure SSL (automatic with Render)

### 2. Monitoring
- Set up health checks
- Monitor application logs
- Set up alerts for downtime

### 3. Security
- Regularly update dependencies
- Monitor database access
- Review environment variables

## Cost Considerations

### Free Tier Limitations
- PostgreSQL: 1GB storage, 97 hours/month
- Web Service: 750 hours/month
- Automatic sleep after inactivity

### Paid Plans
- PostgreSQL: $7/month for Starter
- Web Service: $7/month for Starter
- No sleep, better performance, more resources

## Support Resources

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **PostgreSQL Setup**: [render.com/docs/databases](https://render.com/docs/databases)
- **Environment Variables**: [render.com/docs/environment-variables](https://render.com/docs/environment-variables)

## Quick Checklist

Before deploying, ensure you have:
- [ ] GitHub repository with all code
- [ ] Render account created
- [ ] PostgreSQL database created on Render
- [ ] DATABASE_URL copied
- [ ] HUGGINGFACE_TOKEN obtained
- [ ] requirements.txt updated
- [ ] Streamlit config file created
- [ ] Environment variables ready

## Next Steps

After successful deployment:
1. Test all features thoroughly
2. Set up monitoring and alerts
3. Consider custom domain
4. Plan for scaling if needed
5. Regular backups of database

Your application will be available at: `https://your-app-name.onrender.com`