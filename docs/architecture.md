# AI Fabric — System Architecture

## 1. Purpose

AI Fabric is intended to be an explainable AI execution control plane. It provides a unified model API, analyzes workloads, selects a configured route based on explicit constraints, executes through a provider adapter, and records operational outcomes.

Start as a modular monolith, not premature microservices. This is the target design; components count as implemented only when code and tests verify them.

## 2. Intended request lifecycle

1. Client sends a request.
2. API validates payload and assigns request/execution ID.
3. Workload analyzer derives supported features from request and routing hints.
4. Policy engine applies mode, budget, latency, quality, and privacy constraints.
5. Execution planner selects a configured route and records a human-readable explanation.
6. Provider adapter calls the model endpoint.
7. Reliability layer applies timeouts, bounded eligible retries, and configured fallback.
8. Telemetry records outcome, latency, usage, errors/fallbacks, and decision metadata.
9. API returns the model result and available execution/decision information.

If a feature cannot be inferred reliably, label it as an estimate or accept it as an explicit user hint.

## 3. Logical components

### API layer
FastAPI routes, Pydantic schemas, validation, request IDs, consistent error responses.

### Workload analyzer
Derives task type, context size, estimated token demand, complexity hints, latency preference, budget, quality preference, privacy requirement, and streaming requirement where supported.

### Policy engine and execution planner
Initial modes: `LOW_COST`, `LOW_LATENCY`, `HIGH_QUALITY`, `BALANCED`, `PRIVACY_FIRST`. Explain selected route and constraints. Do not promise private execution unless a suitable private/self-hosted route is configured.

### Provider adapter
Isolates endpoint/model identifiers, authentication, timeout, and response normalization. Credentials come from environment configuration and are never hard-coded.

### Reliability layer
Retries only eligible transient errors, within a strict limit. Fallback only when a compatible alternative exists. Avoid loops and secret-bearing provider errors.

### Persistence
PostgreSQL is planned for execution records, routing decisions, usage, and benchmark metadata. SQLAlchemy/Alembic are planned tools.

### Cache/coordination
Redis may support suitable caching, rate limits, or short-lived coordination. It is not durable execution history; do not add it to request paths without a defined use.

### Observability
Record request ID, route, status, latency, provider-reported token usage, cost estimate and assumptions, retry/fallback outcomes, and policy decision. Never log API keys, auth headers, or raw sensitive prompts by default.

### Dashboard
A planned React/TypeScript dashboard should show actual requests, routes, latency, errors, estimated cost, fallbacks, and security events. Mock data must be labelled.

## 4. Planned API surface

| Method | Path | Purpose | Status |
|---|---|---|---|
| GET | `/health` | Initial health check | Prototype exists; re-test |
| GET | `/v1/health` | Versioned health | Planned |
| POST | `/v1/chat/completions` | OpenAI-compatible model API; `model: "auto"` routes automatically | Prototype exists; evolve with tests |
| POST | `/v1/workloads/execute` | Explicit workload execution | Planned |
| GET | `/v1/executions/{execution_id}` | Execution status/history | Planned |
| GET | `/v1/executions/{execution_id}/decision` | Routing explanation | Planned |
| GET | `/v1/metrics` | Protected metrics | Planned |
| POST | `/v1/benchmarks/run` | Controlled benchmark | Planned |

Define exact schemas, status codes, errors, and authentication in API contract documentation before considering endpoints complete. Keep both chat and workload APIs only if their purposes are distinct.

## 5. Planned execution record

Fields may include execution ID/timestamps, status, provider/model, routing mode and explanation, latency, provider-reported tokens, estimated cost plus source/assumptions, retry/fallback outcomes, and sanitized error category.

Do not store raw prompts by default. If needed later, define retention, access control, redaction, and consent first.

## 6. Security and privacy

- Keep credentials in environment variables or a local ignored `.env`.
- Commit `.env.example` with placeholders only.
- Validate input size and request fields.
- Apply timeouts and bounded retries.
- Redact credentials and sensitive values from logs.
- Restrict metrics/admin endpoints if exposed.
- Do not claim private execution without a configured private route.
- Document limitations and safe failure behavior.

## 7. Testing strategy

- Unit: schemas, workload features, policy rules, planner explanations, cost calculations.
- Provider: mocked success, timeout, auth failure, malformed response.
- Integration: API + database, migrations, Redis if used.
- Reliability: transient/permanent errors, retry budget, fallback success/failure.
- Security: malformed input, secret redaction, metrics access, privacy policy.
- End-to-end: client request through routing/provider.
- Benchmark: repeatable workload, baseline, sample count, P50/P95, errors, limitations.

Mocks test local logic; they do not prove live Nebius/NVIDIA integration.

## 8. Deployment

Local development uses WSL2 Ubuntu and Docker Desktop. Containerization follows stable local tests. Nebius is the intended deployment target, conditional on account access, model endpoint, resources, and current hackathon rules.

## 9. Current implementation caveat

The initial FastAPI app, `/health`, and `/v1/chat/completions` provider-proxy prototype exist. The last reported test run passed four tests. This does not prove PostgreSQL, Redis, intelligent routing, live inference, dashboard, benchmarks, or deployment are complete.
