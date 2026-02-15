# CloudSpend AI Agent

A scalable multi-agent AI system for cloud cost management and optimization across AWS, Azure, and GCP.

## Project Structure

```
cloudspend-ai-agent/
├── backend/                 # Backend API and agent system
│   ├── agents/             # AI agents (Cost Analysis, Optimization, Forecasting)
│   ├── api/                # REST API endpoints
│   ├── core/               # Core orchestration logic
│   ├── services/           # Cloud provider integrations
│   ├── models/             # Data models
│   ├── utils/              # Utility functions
│   ├── config/             # Configuration settings
│   ├── tests/              # Unit tests
│   └── main.py             # Application entry point
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── utils/          # Utility functions
│   │   └── styles/         # CSS styles
│   └── public/             # Static assets
├── infra/                  # Infrastructure as Code
│   ├── docker/             # Docker configurations
│   ├── kubernetes/         # K8s manifests
│   ├── terraform/          # Terraform configs
│   └── scripts/            # Deployment scripts
├── docs/                   # Documentation
│   ├── architecture/       # Architecture docs
│   ├── api/                # API documentation
│   └── guides/             # User guides
└── mock-data/              # Mock data for testing
    ├── aws/                # AWS mock data
    ├── azure/              # Azure mock data
    └── gcp/                # GCP mock data
```

## Features

- 🤖 Multi-agent AI system for intelligent cost analysis
- 📊 Real-time cost monitoring and visualization
- 💡 AI-powered optimization recommendations
- 📈 Cost forecasting and trend analysis
- ☁️ Multi-cloud support (AWS, Azure, GCP)
- 🔄 Scalable microservices architecture

## Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
cd infra/docker
docker-compose up
```

## Architecture

The system uses a multi-agent architecture with specialized agents:
- **Cost Analysis Agent**: Analyzes spending patterns
- **Optimization Agent**: Recommends cost-saving strategies
- **Forecasting Agent**: Predicts future costs

## Documentation

See the [docs](./docs) folder for detailed documentation:
- [Architecture Overview](./docs/architecture/overview.md)
- [API Documentation](./docs/api/endpoints.md)
- [Getting Started Guide](./docs/guides/getting-started.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
