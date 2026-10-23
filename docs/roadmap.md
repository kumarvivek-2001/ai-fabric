# AI Fabric — Development Roadmap

## Goal

Build an explainable AI execution control plane that validates requests, analyzes workloads, selects a suitable configured model route, executes through Nebius/NVIDIA infrastructure, handles failures safely, and records verifiable operational results.

This roadmap preserves the existing six implementation phases and maps the original detailed plan into them. `master-checklist.md` is the task-level source of truth.

## Status labels

- `DONE` — implemented and verified with evidence.
- `IN PROGRESS` — actively being implemented.
- `PENDING` — not yet completed.
- `BLOCKED` — waiting for external access/resource.
- `FUTURE` — tracked for later SaaS scope, not silently forgotten.

Documentation alone does not prove implementation.

## Phase 0 — Product definition and foundation

Define the problem/user, product direction, hackathon requirements, constraints, MVP versus future SaaS scope, and consistent documentation.

**Completion:** product scope and requirements are documented, and status claims are honest.
**Status:** initial docs exist; detailed requirements and official-rule recheck remain.

## Phase 1 — System design

Define request lifecycle, module boundaries, API contracts/errors, workload features, routing modes, PostgreSQL schema, Redis responsibilities, provider capabilities, retry/fallback rules, observability, security/privacy, tests, and benchmark method.

**Completion:** design decisions are recorded and usable during implementation.
**Status:** initial architecture exists; detailed contracts/design docs remain.

## Phase 2 — Coding foundation and persistence

Keep the environment reproducible; evolve the current app without breaking it; verify health/chat endpoints; maintain compatible dependencies; add configuration and `.env.example`; start PostgreSQL/Redis with Compose; implement SQLAlchemy models, Alembic migrations, execution history, routing decisions, and persistence tests.

**Completion:** app/tests work locally and migration/persistence tests pass.
**Status:** FastAPI prototype exists; persistence pending.

## Phase 3 — API contracts and real Nebius/NVIDIA integration

Define schemas and consistent errors; evolve `/v1/chat/completions`; add `model: "auto"` and routing constraints; implement provider adapter; verify a real request through Nebius Token Factory using an eligible NVIDIA open model (or an allowed alternative); test invalid credentials, unavailable model, timeout, and provider errors. Keep mock tests distinct from live integration.

**Completion:** real model request is repeatable, or external access is explicitly marked blocked. A mock does not satisfy live-runtime requirements.
**Status:** proxy prototype exists; live model call not verified.

## Phase 4 — Workload analysis, intelligent routing, and cost policy

Analyze task type, context size, token demand, complexity hints, latency, budget, quality, privacy, and streaming where supported. Implement `LOW_COST`, `LOW_LATENCY`, `HIGH_QUALITY`, `BALANCED`, `PRIVACY_FIRST`; use a capability registry based on verified/configured facts; implement deterministic policy/planning; explain decisions; estimate cost only when pricing/usage data supports it.

**Completion:** different constraints produce tested, explainable decisions.
**Status:** pending.

## Phase 5 — Reliability, observability, security, and dashboard

Add bounded retries for eligible transient errors, fallback only to configured compatible routes, request IDs, safe errors, execution telemetry, secret redaction, input limits, metrics access control, unit/integration/security/end-to-end tests, and a dashboard connected to real data. Add tracing/Prometheus/Grafana only if practical.

**Completion:** failure scenarios are tested, telemetry is real, and sensitive data is not exposed.
**Status:** pending beyond initial endpoint tests.

## Phase 6 — Benchmark, packaging, deployment, and hackathon polish

Create repeatable workloads and baseline; measure P50/P95 latency, failure rate, fallback recovery, tokens, and cost where available; record environment and limitations; build/test Docker image and Compose; deploy to Nebius if access/resources allow; re-check current official rules; prepare public repo/license/README/demo/video; verify every claim and submit before deadline.

**Completion:** another person can run/access the demo and distinguish measurements from estimates.
**Status:** pending.

## Future SaaS scope

Track separately: multi-tenant billing, broad provider marketplace, global Kubernetes/GPU fleet, advanced learned routing, enterprise SSO/compliance certification, and full GPU cloud marketplace. These are deferred, not marked complete, and should not block a reliable hackathon vertical slice.
