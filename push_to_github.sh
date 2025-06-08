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
git commit -m "PharmQAgentAI: Complete user-friendly interface transformation

Latest Updates:
- Eliminated all JSON responses throughout the application
- Replaced with professional dashboard-style displays using metrics and progress bars
- Enhanced 24 pharmaceutical AI agents across 6 categories
- Added visual elements: icons, color-coded status indicators, structured layouts
- Transformed technical data into plain-language explanations
- Comprehensive drug discovery workflow automation
- Advanced decision support with risk assessment and optimization
- Real-time market intelligence and patent analysis
- Multi-modal research capabilities with document processing"

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