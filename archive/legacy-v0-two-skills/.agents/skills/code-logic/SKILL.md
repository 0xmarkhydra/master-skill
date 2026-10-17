---
name: code-logic
description: Enforce production-oriented, minimal, testable coding standards for Next.js BFF/APIs and Go, NestJS or ASP.NET Core backends. Covers API contracts, pagination, SQL injection defense, authentication, authorization, rate limits, daily public-API quotas, consistency, tests and honest execution reporting.
---

# Code Logic — portable software engineering rules

Apply to **every coding task**, especially API, backend, database, auth, tests, integrations and migrations. For significant UI changes also use `ui-v3-design`. This skill is a **policy and checklist**, not executable infrastructure. A rule is implemented only when matching source/config/tests prove it.

## 1. Work like a careful senior engineer

- Inspect Git status, callers, routes, existing contracts, tests, DB schema and actual stack **before** editing. Keep staged/unstaged/untracked or other-agent work safe. No force-push, destructive reset, blind conflict resolution or unapproved production writes.
- Reuse project utilities, platform primitives and installed dependencies. Smallest **complete readable** implementation wins; no speculative abstraction, libraries or settings. Do not remove validation, error handling, access controls or edge cases for brevity.
- Scope the change and find the root cause rather than patching every screen. Update connected callers, tests, docs and schema migration **when genuinely required**. Preserve existing public contracts and data by default.
- On ambiguous high-risk requirements (data deletion, financial logic, public exposure, secrets, billing), pause and ask; otherwise use safe conventional defaults and state assumptions.

## 2. API definition and HTTP behavior

- Design resource-oriented or project-consistent routes, explicit versioning when breaking contracts, request/response DTOs and documented schemas. Never expose database entities or private fields wholesale.
- Use correct methods: GET/HEAD are **read-only** and never change business state; POST creates/executes, PUT replaces, PATCH edits, DELETE deletes subject to authorization. Avoid side-effecting GET.
- Validate all input server-side: type, length, enum, numerical bounds, ownership/scope, object shape, uploaded file type/signature/size, valid state transitions. Reject invalid input with actionable but non-sensitive errors.
- Return meaningful HTTP statuses: 200/201/204, 400 or 422, 401 unauthenticated, 403 forbidden, 404 not found (including privacy-preserving 404 where appropriate), 409 conflict, 429 throttled, 5xx failures. Use a consistent machine-readable error envelope and correlation/trace ID. Never return `200 success` after a failed DB write.
- For mutation requests, enforce authZ **at endpoint and record level**, transactions when multi-step invariants depend on atomicity, concurrency protection, idempotency for payment/retry-sensitive operations and audit trails for consequential actions.
- Handle external calls with sensible timeouts, retries only for safe/idempotent operations, backoff and observable failure; no silent catch/fallback that turns security failure into access.

## 3. Mandatory GetList and pagination

All potentially unbounded collection endpoints (`GetList`, `GetAll`, `Search`, feed/table lists) **MUST paginate on the server**. Bounded tiny lookup tables, aggregates and explicitly scoped exports are documented exceptions.

**Request baseline:** `GET /api/v1/resources?page=1&pageSize=25&search=...&sortBy=createdAt&sortDir=desc`. Allow pageSize 10/25/50/100, default 25, maximum 100; cursor pagination for fast-changing feeds or large offset workloads. Validation/normalization must be consistent.

**Execution order:** determine authenticated tenant/user record scope → validate filters and sort columns against whitelist → filter by authorized scope **in the DB query** → count filtered permitted rows (when contract needs a count) → stable unique ordering → LIMIT/OFFSET or signed/validated cursor. Do not `SELECT *` all rows, then paginate with array slice. Count must not reveal rows user cannot access. Avoid N+1 queries and bound expensive search.

**Response baseline:** `{ "items": [], "page": 1, "pageSize": 25, "totalCount": 0, "totalPages": 0, "hasPrevious": false, "hasNext": false }`. Never silently change older array responses: version/adapter and migrate clients. For cursors use `nextCursor` and document absent/optional totalCount. Validate empty, page=last, page>last, sort/filter changes, cross-tenant attacks, export semantics and performance with large fixtures.

## 4. SQL and data integrity

- Always use bound SQL parameters/prepared queries or safe ORM query APIs. **Never concatenate user values into SQL**. Dynamic table/column/sort identifiers must come from explicit allowlists, never user string interpolation.
- Avoid injection in SQL and equivalent NoSQL/ORM/raw-filter surfaces. Restrict returned columns; never return secret, payroll, identity, keys or banking fields unless specifically authorized. Prevent IDOR on read, write and file download.
- Use migrations for schema changes; review indexes, keys, uniqueness, foreign keys, transaction isolation and rollout/backfill for relevant operations. Back up and test restore before destructive data changes.
- Design for real concurrency: unique constraints, optimistic locking or transaction isolation as needed; avoid check-then-write races. Preserve money precision, time zones and auditability.
- Never print `.env`, token, DB connection string, personal records or sensitive request bodies in logs. Secrets come from secure env/secret manager.

## 5. Authentication, public access and rate limits

**Mandatory by category:**
- **Login / registration / MFA / password reset / OTP:** apply server/edge **rate limiting** and abuse detection. Combine layered controls (source/IP + normalized account/identifier where applicable), credential-failure handling, non-enumerating responses, cooldown, logging/metrics and verified lockout UX. Avoid permanent denial-of-service against shared IPs/users. Never skip protection because the screen is “internal”.
- **Public GET APIs:** apply bounded burst and sustained rate limits; additionally define **daily quota** when endpoint is anonymous, expensive or metered. Quota key prefers authenticated client/API key/customer; for anonymous callers fall back to carefully normalized IP plus anti-abuse controls. State timezone/window semantics (e.g. rolling 24h or UTC day), quotas and reset behavior explicitly. Do not invent a universal requests-per-day number: configure by expected traffic and resource cost.
- **Sensitive/high-cost APIs** (search, exports, file presign/upload, AI provider, messaging, bulk writes, data scraping): tighter per-user/tenant/API-key/IP policies and budget or concurrency caps according to impact.
- Response on rejection: **429**, optional standard `RateLimit-*` headers and `Retry-After`/reset when possible; standardized error, metrics and no secret leakage. Quota checks must not be bypassable by arbitrary client-supplied headers.
- **Distributed deployments:** use shared atomic storage such as Redis/managed gateway for global quotas, not per-process RAM if consistency matters. Authenticate actual source IP through **trusted proxy** configuration. Decide fail-open vs fail-closed based on abuse/security impact and document the tradeoff.
- Distinguish **daily quota** from burst protection: both are needed for abusive public endpoints. Cache public GET responses where safe without leaking user data. Test boundaries and parallel requests.

See `references/API-SECURITY.md` and `references/STACK-ADAPTERS.md`.

## 6. Application security

- Authenticate server-side; authorize by resource, tenant, owner and action. UI visibility is not authorization.
- For cookie sessions: use HttpOnly/Secure/SameSite as appropriate, server-side expiry/revocation and CSRF defense for state-changing requests; defend against XSS. For bearer auth use short-lived, correctly validated credentials and secure storage; **do not place long-lived sensitive tokens in browser localStorage** by default.
- Least privilege for DB/storage/service credentials; allowed origins for CORS rather than wildcard with credentials; sane CSP/security headers; validate outbound URLs/IPs to prevent SSRF; enforce upload/attachment size/type policies and safe authorization on every download.
- Hide internal exception details from clients; preserve traceability server-side without logging secrets. Threat-model high-risk actions, payment and identity flows.

## 7. Stack-aware boundaries

- **Next.js frontend + BFF:** enforce real auth/session in route handlers/server actions, keep secret credentials server-only, never treat middleware or a hidden button as the only permission gate, use server-side validation and CSRF/origin safeguards suited to auth type.
- **NestJS:** modules/controllers/services/repositories according to current structure; DTO validation pipes and guard/policy for authZ, server-side rate-limit middleware/guards, parameterized query or configured ORM, proper exception filters; avoid exporting unsafe entities.
- **Go:** idiomatic `net/http` or existing router, context cancellation, middleware for auth/rate limits, `database/sql` parameter placeholders or safe query builder, explicit errors/timeouts and race-aware transactions. Avoid global mutable per-process rate counters for shared quotas.
- **ASP.NET Core:** endpoint authorization policies/filters, model validation, antiforgery for cookie-authenticated writes, built-in rate limiting, safe EF parameterization or ADO.NET parameters, async DB access and cancellation.
- No forced architecture switch. Adapt named layers to the actual code; do not claim a framework feature exists without inspecting its installed version.

## 8. Verification — no pretend success

For each task identify success **and failure** paths. Test invalid input, 401/403, cross-record scope, SQL injection payload, pagination boundaries, rate-limit 429/quota resets and concurrency as relevant. Run lint/typecheck/build, focused unit/integration/contract tests; browser flows when actual test runtime is available. Never touch real production data for convenience.

**Tool-grounded truth:** a requested action is not successful because an AI wrote code or issued a tool call. Wait for the result, read exit code and effects, verify persisted state and remote deployment separately. If no execution happened use `NOT RUN`; if a tool denies access use `BLOCKED`. Never claim green CI/UAT, push, merge or deploy without actual evidence. Test mocks are not live service verification.

Before handoff report changed files, exact checks and results, risk, compatibility and any unverified behavior. Shortcuts with known ceilings must include upgrade triggers rather than hidden technical debt.
