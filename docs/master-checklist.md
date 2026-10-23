# AI Fabric — Master Checklist

Task-level tracker for the original detailed plan and the six delivery phases. Change status only after checking code, test output, or external evidence.

## Status legend
- `DONE` — implemented and verified.
- `IN PROGRESS` — being worked on.
- `PENDING` — not complete.
- `BLOCKED` — requires external access/resource.
- `FUTURE` — tracked for later SaaS scope.

## Phase 0 — Product and hackathon requirements
- [x] Choose AI Fabric / AI execution-control-plane direction.
- [x] Initial README, architecture, setup, and roadmap exist.
- [ ] Write product spec and target-user/problem statement.
- [ ] Write hackathon requirements/compliance checklist.
- [ ] Re-check current official rules before submission.
- [ ] Separate hackathon MVP from future SaaS.
- [ ] Track external dependencies and status.

## Phase 1 — System design
- [x] Initial request flow and component ideas documented.
- [ ] Define API contracts and standard error format.
- [ ] Define module boundaries.
- [ ] Define workload features and estimated fields.
- [ ] Define routing modes and decision explanation schema.
- [ ] Define PostgreSQL schema/migrations.
- [ ] Define Redis use cases.
- [ ] Define provider capability registry.
- [ ] Define retry/fallback policy and request-ID behavior.
- [ ] Define observability and benchmark method.
- [ ] Define security/privacy and testing strategy.
- [ ] Review design against the actual MVP.

## Phase 2 — Coding foundation and persistence
- [x] Project folder, Git repository, and virtual environment exist.
- [x] FastAPI app and `/health` endpoint implemented.
- [x] Initial chat-completions proxy prototype implemented.
- [x] Previous local test run: 4 passed (re-run after changes).
- [ ] Inspect Git diff before modifying code.
- [ ] Create/verify compatible `requirements.txt`.
- [ ] Add configuration module and `.env.example`.
- [ ] Organize app modules incrementally.
- [ ] Re-run health and existing tests.
- [ ] Add Compose for PostgreSQL and Redis.
- [ ] Verify database/cache health.
- [ ] Add SQLAlchemy models/session.
- [ ] Add Alembic and first migration.
- [ ] Persist execution and routing-decision records.
- [ ] Add persistence integration tests.

## Phase 3 — API and live provider integration
- [ ] Define request/response schemas.
- [ ] Preserve and test `/v1/chat/completions`.
- [ ] Add/document `model: "auto"` and routing constraints.
- [ ] Decide whether `/v1/workloads/execute` is distinct or mapped.
- [ ] Check Nebius Token Factory account/model access.
- [ ] Verify eligible NVIDIA model ID and current API docs.
- [ ] Configure credentials without committing secrets.
- [ ] Implement provider adapter.
- [ ] Make a real model request and save safe evidence.
- [ ] Test bad credentials, unavailable model, timeout, provider errors.
- [ ] Label mock tests separately from live integration.

## Phase 4 — Analyzer, routing, and cost policy
- [ ] Implement workload analyzer.
- [ ] Implement `LOW_COST`, `LOW_LATENCY`, `HIGH_QUALITY`, `BALANCED`, `PRIVACY_FIRST`.
- [ ] Define verified model capability registry.
- [ ] Implement deterministic policy engine and planner.
- [ ] Add “why this route?” explanation.
- [ ] Respect constraints or return no-compatible-route explicitly.
- [ ] Track usage/cost only when source data supports it.
- [ ] Test modes, conflicting constraints, unsupported capabilities.
- [ ] Verify `model: "auto"` calls the policy path.

## Phase 5 — Reliability, observability, security
- [ ] Classify transient/permanent errors.
- [ ] Add bounded retries/backoff for eligible transient errors.
- [ ] Add fallback only to a configured compatible alternative.
- [ ] Test fallback success and failure.
- [ ] Add request IDs and sanitized errors.
- [ ] Record status, route, latency, tokens, cost estimate, retry/fallback.
- [ ] Ensure logs do not expose keys, auth headers, sensitive prompts.
- [ ] Add input-size limits and validation.
- [ ] Protect metrics/admin routes if exposed.
- [ ] Add security/privacy tests.
- [ ] Add structured logs and practical metrics.
- [ ] Add tracing/Prometheus/Grafana if practical.
- [ ] Build dashboard from real backend data; label fixtures.
- [ ] Test dashboard loading/error/empty states.

## Phase 6 — Benchmark, packaging, deployment, submission
- [ ] Define repeatable benchmark workload and baseline.
- [ ] Measure P50/P95 latency, failure rate, fallback recovery, tokens, cost where available.
- [ ] Record environment, request count, warm-up, limitations.
- [ ] Do not publish invented metrics/savings.
- [ ] Add Dockerfile and Compose configuration.
- [ ] Run app in a container and verify health.
- [ ] Confirm Nebius deployment prerequisites/access.
- [ ] Deploy to Nebius if resources/access allow.
- [ ] Re-check current official rules.
- [ ] Confirm public repository and open-source license.
- [ ] Complete README setup and architecture.
- [ ] Prepare real demos: efficient route, reasoning route, budget constraint, controlled failure/fallback, security policy.
- [ ] Record video within current official time limit.
- [ ] Clearly explain Nebius and NVIDIA model usage.
- [ ] Submit before deadline and retain confirmation.

## Mapping from older detailed phase numbers

Original product definition/foundation → Phase 0.  
Original architecture/API/database/security/testing design → Phase 1.  
Original coding foundation/API/persistence → Phase 2.  
Original NVIDIA/Nebius integration → Phase 3.  
Original workload analyzer/router/cost optimizer → Phase 4.  
Original retries/fallback/observability/security/dashboard/demo scenarios → Phase 5.  
Original benchmark/deployment/release review/video → Phase 6.

Older notes use inconsistent phase numbers for dashboard, demo, benchmark, deployment, and video. This mapping preserves the tasks without silently dropping or renumbering them.

## Future SaaS scope — tracked, not hackathon blockers
- [ ] Multi-tenant organization/account model.
- [ ] Production-grade API-key lifecycle and quotas.
- [ ] Billing/subscriptions/invoices.
- [ ] Broad provider marketplace.
- [ ] Global Kubernetes/GPU fleet.
- [ ] Advanced learned/online routing.
- [ ] Enterprise SSO/formal compliance certification.
- [ ] Full GPU cloud marketplace.

These are deferred, not completed, and should not block the focused hackathon vertical slice.
