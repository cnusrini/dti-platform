# PharmQAgentAI - High-Level Architecture

## System Overview
PharmQAgentAI is a comprehensive therapeutic intelligence platform that combines AI-powered drug discovery with advanced pharmaceutical research capabilities. The platform uses a modular, scalable architecture built on Streamlit with Google AI integration.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PharmQAgentAI Platform                       │
├─────────────────────────────────────────────────────────────────┤
│                     Frontend Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Streamlit UI  │  │  User Interface │  │ Authentication  │ │
│  │   (frontend/)   │  │   Components    │  │    System       │ │
│  │                 │  │                 │  │   (auth/)       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Business Logic Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Prediction     │  │   AI Agents     │  │   Workflow      │ │
│  │   Engines       │  │   (24 Agents)   │  │  Management     │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                     Backend Services                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Model Manager  │  │  Data Processing│  │   Validation    │ │
│  │   (models/)     │  │    (utils/)     │  │   Services      │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    External Integrations                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Google AI     │  │  Hugging Face   │  │   Chemical      │ │
│  │     APIs        │  │    Models       │  │   Databases     │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend Layer (`frontend/`)
- **Main Application**: `frontend/app.py` - Primary Streamlit interface
- **Advanced Agents UI**: `frontend/advanced_agent_interface.py` - Specialized agent interfaces
- **Streamlit Components**: Custom UI components and styling

### 2. Authentication System (`auth/`)
- **User Management**: `auth/user_management.py` - User registration, login, subscriptions
- **Landing Page**: `auth/landing_page.py` - Public interface and pricing
- **Database**: SQLite-based user and subscription management

### 3. AI Agents System (`backend/agents/`)
- **Agent Manager**: `agent_manager.py` - Orchestrates all AI agents
- **24 Specialized Agents**:
  - **Workflow Automation** (4 agents): Pipeline, Data Collection, Quality Control, Knowledge Update
  - **Collaborative Research** (4 agents): Collaboration Setup, Market Analysis, Patent Search, Regulatory
  - **Real-Time Intelligence** (4 agents): Pattern Recognition, Biomarker Discovery, Safety Monitoring, Clinical Insights
  - **Advanced Analytics** (4 agents): Document Processing, Literature Analysis, Data Mining, Predictive Analytics
  - **Multi-Modal Research** (4 agents): Image Analysis, Text Processing, Molecular Visualization, Report Generation
  - **Decision Support** (4 agents): Risk Assessment, Treatment Optimization, Drug Repurposing, Clinical Decision

### 4. Prediction Engines (`models/`, `backend/models/`)
- **Model Manager**: Handles loading and management of transformer models
- **Prediction Tasks**: 
  - **DTI**: Drug-Target Interaction prediction
  - **DTA**: Drug-Target Affinity calculation
  - **DDI**: Drug-Drug Interaction analysis
  - **ADMET**: Absorption, Distribution, Metabolism, Excretion, Toxicity properties
  - **Similarity**: Molecular similarity search

### 5. Utilities & Validation (`utils/`, `backend/utils/`)
- **Molecular Utils**: SMILES validation, molecular property calculation
- **Validation**: Input validation for all prediction tasks
- **Model Preloader**: Background model loading and caching

### 6. Configuration (`config/`, `backend/config/`)
- **Model Registry**: Central registry of available models
- **API Configuration**: External service configurations

## Technology Stack

### Core Framework
- **Streamlit**: Web application framework
- **Python 3.11**: Primary programming language

### AI/ML Components
- **Google AI**: Gemini models for agent intelligence
- **Hugging Face Transformers**: 20+ transformer models for predictions
- **PyTorch**: Deep learning framework

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations

### External APIs
- **Google AI API**: Powers the 24 AI agents
- **Hugging Face Hub**: Model repository access

## Data Flow

### 1. User Interaction Flow
```
User Input → UI Validation → Business Logic → AI Processing → Results Display
```

### 2. Prediction Workflow
```
SMILES/Sequence → Validation → Model Selection → Inference → Post-processing → Visualization
```

### 3. AI Agent Workflow
```
User Query → Agent Selection → Context Building → AI Processing → Result Synthesis → Response
```

## Key Features

### 1. Prediction Capabilities
- **Multi-Model Support**: 20+ transformer models
- **Real-Time Processing**: Instant predictions with caching
- **Batch Processing**: Multiple compound analysis
- **Results Visualization**: Interactive charts and tables

### 2. AI Agent Intelligence
- **Natural Language Processing**: Query understanding and response generation
- **Multi-Agent Coordination**: Collaborative problem solving
- **Domain Expertise**: Pharmaceutical and biomedical knowledge
- **Adaptive Learning**: Context-aware responses

### 3. User Experience
- **Professional UI**: Clean, medical-grade interface
- **Responsive Design**: Works across devices
- **Real-Time Updates**: Live prediction status
- **Data Export**: Results download capabilities

## Deployment Architecture

### Current Setup
- **Platform**: Replit Cloud Environment
- **Runtime**: Python 3.11 with Nix package management
- **Port**: 5000 (configured for external access)
- **Process Management**: Streamlit server with auto-restart

### External Deployments
- **Render**: Production deployment at dti-platform-v1.onrender.com
- **GitHub Integration**: Version control and CI/CD ready

## Security & Performance

### Security Features
- **User Authentication**: Secure login/registration system
- **Subscription Management**: Role-based access control
- **API Key Management**: Secure external service integration
- **Input Validation**: Comprehensive data sanitization

### Performance Optimizations
- **Model Caching**: Preloaded models for faster inference
- **Session Management**: Persistent user state
- **Async Processing**: Non-blocking AI operations
- **Resource Management**: Efficient memory usage

## Scalability Considerations

### Current Capacity
- **Concurrent Users**: Optimized for research teams
- **Model Performance**: Sub-second predictions
- **Agent Responsiveness**: Real-time AI interactions

### Future Enhancements
- **Microservices**: Backend service separation
- **Database Scaling**: PostgreSQL migration ready
- **Container Deployment**: Docker support available
- **Load Balancing**: Multi-instance deployment capable

---

*This architecture supports both individual researchers and enterprise pharmaceutical teams with comprehensive drug discovery capabilities.*