# AI Fabric

**An intelligent AI Gateway for reliable, observable, and cost-aware model access.**

AI Fabric is a proposed AI infrastructure platform that aims to provide a unified API for accessing AI models, with a foundation for routing, observability, reliability, and cost management.

## Goals

- Provide a unified interface for AI model requests.
- Support configurable model routing.
- Track request latency, errors, and token usage where available.
- Make model providers and deployment configuration easy to change.
- Establish a foundation for reliability and cost-aware routing.

## Initial Scope

1. Project architecture and development documentation.
2. Gateway API and request validation.
3. Integration with a selected AI model provider.
4. Request logging and observability.
5. Routing policies and failure handling.
6. Containerized local development and deployment preparation.

## Technology Direction

- **Language:** Python
- **API:** FastAPI
- **Containers:** Docker and Docker Compose
- **Version control:** Git
- **Model integration:** NVIDIA-compatible model endpoint
- **Deployment target:** Nebius infrastructure, subject to available credits and deployment requirements

Technology choices may evolve as implementation and testing progress.

## Project Status

Phase 0 — Foundation and documentation.

Implementation, benchmarks, and deployment are not yet complete.

## Repository Structure

```text
ai-fabric/
├── README.md
└── docs/
    ├── architecture.md
    ├── development-setup.md
    └── roadmap.md
```

## Development Principle

Document verified behavior, measure performance rather than guessing, and keep secrets out of source control.
