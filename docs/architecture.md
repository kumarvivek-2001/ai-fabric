# AI Fabric — System Architecture

## 1. Purpose

AI Fabric is an AI gateway designed to provide a unified interface for AI model access, request routing, observability, and reliability.

The initial version will prioritize a small, testable system before adding advanced routing and optimization.

## 2. High-Level Request Flow

1. A client sends an HTTP request to the AI Fabric API.
2. The gateway validates the request.
3. The routing layer selects a configured model provider.
4. The provider adapter sends the request to the model endpoint.
5. The gateway returns the model response to the client.
6. The gateway records request status, latency, and available usage information.

## 3. Core Components

### API Layer
- Built with FastAPI.
- Exposes health and model-inference endpoints.
- Validates incoming requests and returns structured errors.

### Routing Layer
- Selects a configured provider and model.
- Starts with a simple default routing policy.
- Can later support latency, availability, and cost-aware policies.

### Provider Adapter
- Isolates provider-specific API details from the gateway.
- Keeps provider configuration outside core routing logic.
- Reads credentials from environment variables.

### Observability
- Records request outcomes, latency, and errors.
- Captures token usage when the provider returns it.
- Avoids logging API keys or sensitive request content.

### Reliability
- Applies request timeouts.
- Handles provider errors gracefully.
- Can later support retries, fallback providers, and rate limiting.

## 4. Initial API Design

### GET /health
Returns a health status for the gateway process.

### POST /v1/chat/completions
Accepts a model identifier and chat messages, forwards the request to a configured provider, and returns the response.

The exact request and response schema will be finalized during implementation.

## 5. Initial Technology Choices

- Python
- FastAPI
- HTTPX for outbound HTTP requests
- Docker and Docker Compose
- Git
- A configured NVIDIA-compatible model endpoint
- Nebius infrastructure as a deployment target, subject to access and availability

## 6. Security Principles

- Never commit API keys or access tokens.
- Use environment variables for secrets.
- Validate requests before forwarding them.
- Set sensible request timeouts.
- Avoid logging secrets or sensitive user content.

## 7. Planned Evolution

1. Working local API and health endpoint.
2. Model provider integration.
3. Structured request logs and basic metrics.
4. Routing policies and failure handling.
5. Tests, containerization, and deployment.
6. Measured performance evaluation and documentation.

## 8. Current Status

This document describes the planned architecture. Components are not considered implemented until they have been coded and tested.
