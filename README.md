# AI Fabric

**An explainable AI execution control plane for model routing, reliability, and observability.**

AI Fabric is intended to provide a unified model API, analyze workloads, select a configured route based on explicit constraints, explain the decision, execute through a provider adapter, and record operational outcomes.

## Current status

- [x] Initial FastAPI application and `/health` endpoint implemented.
- [x] Initial `/v1/chat/completions` provider-proxy prototype implemented.
- [x] Initial automated tests previously passed locally (4 tests; re-run after changes).
- [ ] Real Nebius Token Factory + NVIDIA open-model request verified.
- [ ] PostgreSQL persistence and Redis integration.
- [ ] Workload analysis and explainable routing.
- [ ] Bounded retries, fallback, and failure-path tests.
- [ ] Usage, latency, cost estimates, and operational metrics.
- [ ] Security/privacy policy checks.
- [ ] Dashboard connected to real backend data.
- [ ] Reproducible benchmark, container verification, and deployment.
- [ ] Final hackathon compliance review and demo submission.

See [`docs/master-checklist.md`](docs/master-checklist.md) for task-by-task tracking. Documentation alone does not prove implementation.

## Intended request flow

1. Client submits a request.
2. API validates it and assigns a request/execution ID.
3. Workload analyzer derives supported workload features.
4. Policy engine evaluates mode and user constraints.
5. Execution planner selects a configured route and explains why.
6. Provider adapter calls the model endpoint.
7. Reliability layer handles eligible timeouts/errors and configured fallback.
8. Execution outcomes, latency, usage, and routing decisions are recorded.
9. API returns the result and available trace/decision information.

The initial implementation should remain a modular monolith. Planned components are not necessarily implemented yet.

## Planned API surface

- `GET /health` — initial health endpoint.
- `GET /v1/health` — planned versioned health endpoint.
- `POST /v1/chat/completions` — existing prototype; `model: "auto"` will become the automatic-routing entry point.
- `POST /v1/workloads/execute` — planned workload-execution contract.
- `GET /v1/executions/{execution_id}` — planned execution status/history.
- `GET /v1/executions/{execution_id}/decision` — planned routing explanation.
- `GET /v1/metrics` — planned protected metrics endpoint.
- `POST /v1/benchmarks/run` — planned benchmark operation.

Exact contracts must be documented before endpoints are considered complete. Evolve the existing prototype with tests; do not delete working code just to match a future design.

## Planned stack

Python, FastAPI, Pydantic, HTTPX, asyncio; PostgreSQL, SQLAlchemy, Alembic; Redis where justified; Nebius Token Factory with at least one eligible NVIDIA open model; pytest; Docker/Compose; structured logs and practical metrics; optionally React/TypeScript for a dashboard; Nebius deployment subject to access and resources.

## Local development

From Ubuntu/WSL:

```bash
cd ~/ai-fabric
source .venv/bin/activate
python -m pytest -v
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for API docs. Stop the server with `Ctrl+C`. Follow [`docs/development-setup.md`](docs/development-setup.md). Keep real credentials in a local ignored `.env`; never commit API keys.

## Documentation

- [`docs/roadmap.md`](docs/roadmap.md) — delivery phases.
- [`docs/master-checklist.md`](docs/master-checklist.md) — detailed task tracker.
- [`docs/architecture.md`](docs/architecture.md) — intended architecture and caveats.
- [`docs/development-setup.md`](docs/development-setup.md) — local setup.

## Working principles

1. Implement in small, testable steps.
2. Verify each step before marking it complete.
3. Never invent benchmark numbers, capabilities, deployment status, or savings.
4. Never log secrets or commit credentials.
5. Mark external dependencies `BLOCKED`/`PENDING` with the reason; never silently skip them.
6. Keep hackathon MVP work separate from future SaaS expansion.
