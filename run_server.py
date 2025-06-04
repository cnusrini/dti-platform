#!/usr/bin/env python3
"""
Simple server script for deploying PharmQAgentAI on Render
"""
import os
import subprocess
import sys

def main():
    """Run the Streamlit application"""
    port = os.environ.get('PORT', '5000')
    
    # Run streamlit with proper configuration for Render
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 
        'frontend/app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()