# AI Fabric — Development Roadmap

## Project Goal

Build an AI gateway that provides a unified model API, configurable routing, useful observability, and reliable request handling.

The project will prioritize working software, reproducible tests, measurable results, and clear documentation.

## Phase 0 — Foundation and Documentation

- [x] Create the project directory.
- [x] Create the documentation directory.
- [x] Write the project README.
- [x] Document the proposed architecture.
- [x] Document the development setup.
- [ ] Document the project roadmap.

**Completion criterion:** The initial project documentation is present and reviewed.

## Phase 1 — Local Development Foundation

- [ ] Inspect the Python environment.
- [ ] Create and activate a Python virtual environment.
- [ ] Add application dependencies.
- [ ] Establish the application package structure.
- [ ] Create a FastAPI application.
- [ ] Implement a health endpoint.
- [ ] Add an initial automated test.
- [ ] Run the application locally and verify the test.

**Completion criterion:** The application starts locally, the health endpoint responds correctly, and the test passes.

## Phase 2 — Model Integration

- [ ] Define request and response schemas.
- [ ] Implement the chat-completions API.
- [ ] Add a provider adapter.
- [ ] Configure a compatible NVIDIA model endpoint.
- [ ] Load credentials from environment variables.
- [ ] Test a real model request when endpoint access is available.
- [ ] Handle invalid requests and provider errors.

**Completion criterion:** A valid request can reach the configured model and return a response, or an explicitly tested mock is used when the external endpoint is unavailable.

## Phase 3 — Routing and Reliability

- [ ] Add configurable model selection.
- [ ] Implement request timeouts.
- [ ] Add safe error handling.
- [ ] Implement bounded retries where appropriate.
- [ ] Add fallback routing if a second provider is available.
- [ ] Test routing and failure scenarios.

**Completion criterion:** Routing decisions and failure behavior are tested and documented.

## Phase 4 — Observability

- [ ] Record request status and latency.
- [ ] Track errors and available token usage.
- [ ] Add structured logs.
- [ ] Add basic metrics.
- [ ] Prevent credentials and sensitive content from appearing in logs.
- [ ] Measure baseline performance.

**Completion criterion:** Test results and measurements can be reproduced.

## Phase 5 — Containerization and Deployment

- [ ] Create a Dockerfile.
- [ ] Add Docker Compose configuration if useful.
- [ ] Build and run the application in a container.
- [ ] Verify health checks and configuration.
- [ ] Prepare deployment on Nebius, subject to account access and available resources.
- [ ] Document deployment and troubleshooting.

**Completion criterion:** The container works locally and any completed remote deployment is verified.

## Phase 6 — Hackathon Polish

- [ ] Add automated tests for key behavior.
- [ ] Run repeatable performance experiments.
- [ ] Document the architecture and design decisions.
- [ ] Prepare a clear demo.
- [ ] Record actual results without inventing benchmarks.
- [ ] Review the hackathon submission requirements.
- [ ] Prepare the final project description and demo materials.

**Completion criterion:** The project can be demonstrated, its core claims are verifiable, and the submission materials are ready.

## Working Principles

1. Implement and test one component at a time.
2. Keep secrets out of source control.
3. Measure performance rather than guessing.
4. Distinguish planned features from implemented features.
5. Prioritize a reliable end-to-end demo before adding unnecessary complexity.

## Current Status

The project is currently in the foundation and documentation stage. Application functionality, performance benchmarks, and deployment remain pending until implemented and verified.
