#!/bin/bash

# PharmQAgentAI GitHub Deployment Script
# This script pushes your enhanced therapeutic intelligence platform to GitHub

echo "Starting GitHub deployment for PharmQAgentAI..."

# Initialize git repository
echo "Initializing git repository..."
git init

# Add all files to git
echo "Adding all files..."
git add .

# Create commit with descriptive message
echo "Creating commit..."
git commit -m "PharmQAgentAI: Enhanced therapeutic intelligence platform

Features:
- 20 verified transformer models from Hugging Face
- Enhanced table-based results display for non-technical users
- Color-coded safety indicators (green/yellow/red)
- Plain language clinical interpretations
- Complete sample data system with authentic pharmaceutical compounds
- Professional backend/frontend architecture
- ADMET properties with safety assessments
- Drug-target interaction predictions with clinical insights"

# Add your GitHub repository as remote
echo "Adding GitHub repository as remote..."
git remote add origin https://github.com/cnusrini/dti-platform.git

# Create main branch and push
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "Deployment complete! Your PharmQAgentAI platform is now on GitHub."
echo "Repository URL: https://github.com/cnusrini/dti-platform"
echo ""
echo "Next steps:"
echo "1. Go to share.streamlit.io to deploy your app"
echo "2. Connect your GitHub repository"
echo "3. Set main file: frontend/app.py"
echo "4. Add HUGGINGFACE_TOKEN to secrets"
echo "5. Deploy and share your enhanced platform"