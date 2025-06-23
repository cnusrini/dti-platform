# PharmQAgentAI: Therapeutic Intelligence Platform

## Overview

PharmQAgentAI is a comprehensive AI-driven therapeutic intelligence platform that combines advanced molecular prediction capabilities with intelligent agent systems for drug discovery research. The platform features a modular architecture with 24 specialized AI agents, 20 transformer models, and comprehensive pharmaceutical analysis tools.

## System Architecture

### Frontend Architecture
- **Technology**: Streamlit-based web application
- **Main Entry Points**: 
  - `frontend/app.py` - Primary enhanced interface with professional styling
  - `frontend/streamlit_app.py` - API-connected frontend for backend integration
  - `app.py` - Legacy unified application
- **Styling**: Custom CSS matching modern pharmaceutical UI/UX standards
- **Components**: Modular UI components with enhanced table displays and clinical interpretations

### Backend Architecture
- **Framework**: FastAPI REST API
- **Main API**: `backend/api/main.py` - Comprehensive API endpoints
- **Architecture Pattern**: Clean separation of concerns with dedicated modules:
  - Models layer for AI model management
  - Utils layer for data processing and validation
  - Agents layer for AI agent orchestration
  - Config layer for model registry and settings

### Multi-Agent System
- **Agent Categories**: 5 main categories with 24 specialized agents
- **Google AI Integration**: Advanced agents using Google Gemini and generative AI
- **Capabilities**: Workflow automation, collaborative research, real-time intelligence, advanced analytics, multi-modal research

## Key Components

### 1. Model Management System
- **Location**: `backend/models/model_manager.py`
- **Purpose**: Handles loading and caching of 20 transformer models from Hugging Face
- **Features**: Dynamic model loading, memory management, model preloading capabilities
- **Model Registry**: Centralized configuration in `backend/config/model_registry.py`

### 2. Prediction Engine
- **Location**: `backend/models/prediction_tasks.py`
- **Supported Tasks**:
  - Drug-Target Interaction (DTI)
  - Drug-Target Affinity (DTA) 
  - Drug-Drug Interaction (DDI)
  - ADMET properties prediction
  - Molecular similarity analysis
- **Output Format**: Professional dashboard-style displays with clinical interpretations

### 3. AI Agent System
- **Base Agent**: `backend/agents/base_agent.py` - Foundation using Google Gemini
- **Agent Manager**: `backend/agents/agent_manager.py` - Orchestrates all agents
- **Specialized Systems**: Multiple agent implementations for different research workflows
- **Google AI Integration**: Uses Google's generative AI for advanced pharmaceutical research

### 4. Validation and Utilities
- **Molecular Utils**: SMILES validation, protein sequence validation, molecular data processing
- **Input Validation**: Comprehensive validation for all prediction tasks
- **Model Preloader**: Background model loading for improved performance

## Data Flow

1. **User Input** → Frontend interface captures molecular data (SMILES, protein sequences)
2. **Validation** → Input validation through `utils/validation.py`
3. **Model Loading** → Dynamic model loading via `ModelManager`
4. **Prediction** → Task-specific prediction through `PredictionTasks`
5. **Agent Processing** → Optional AI agent analysis for enhanced insights
6. **Results Display** → Professional dashboard with clinical interpretations

## External Dependencies

### Required APIs
- **Hugging Face**: Transformer model access (requires `HUGGINGFACE_TOKEN`)
- **Google AI**: Agent system functionality (requires `GOOGLE_AI_API_KEY`)

### Core Dependencies
- **Streamlit** (≥1.45.0) - Frontend framework
- **FastAPI** (≥0.104.0) - Backend API framework
- **PyTorch** (≥2.1.0) - Model inference
- **Transformers** (≥4.36.0) - Hugging Face model integration
- **Pandas/Numpy** - Data processing

### AI Framework Integration
- **Google Generative AI** - Advanced agent capabilities
- **LangChain** - Agent orchestration
- **Anthropic** - Additional AI model support

## Deployment Strategy

### Primary Deployment Options

1. **Streamlit Cloud** (Recommended)
   - Use `frontend/app.py` as main file
   - Add `HUGGINGFACE_TOKEN` to secrets
   - Automatic deployment from GitHub

2. **Replit Deployment**
   - Pre-configured with `.replit` file
   - Run: `streamlit run frontend/app.py --server.port 5000`
   - Port configuration: 5000 (external: 80)

3. **Docker/Container Deployment**
   - Uses `Procfile` for Heroku-style deployments
   - `requirements.txt` for dependency management
   - Environment variable configuration

### Configuration Files
- `.replit` - Replit deployment configuration
- `Procfile` - Process configuration for cloud platforms
- `runtime.txt` - Python version specification
- `.streamlit/config.toml` - Streamlit-specific settings

### Environment Variables
- `HUGGINGFACE_TOKEN` - Required for model access
- `GOOGLE_AI_API_KEY` - Optional for advanced agent features
- `PORT` - Deployment port (defaults to 5000)

## Recent Changes

### June 23, 2025
- Successfully restored PharmQAgentAI to original working state
- Application now fully functional matching dti-platform-v1.onrender.com
- All prediction interfaces (DTI, DTA, DDI, ADMET, Similarity) operational
- 24 AI agents system working correctly
- Professional tabular displays and styling restored
- Created comprehensive architecture documentation (ARCHITECTURE.md)
- Developed detailed project story (PROJECT_STORY.md) covering inspiration, learning, development process, and challenges

### Project Architecture Completed
- Documented complete system architecture with visual diagrams
- Detailed component breakdown across frontend, backend, and AI systems
- Technology stack and deployment strategy fully outlined
- High-level overview suitable for technical presentations and documentation

## User Preferences

Preferred communication style: Simple, everyday language.
Focus on practical solutions and clear explanations.
Document architectural decisions and successful implementations promptly.