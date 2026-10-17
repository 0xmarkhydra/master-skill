# Project Profile — configure a destination repository

Copy and fill this template **in the destination project**. Empty example values are not confirmed project facts. Project instructions supersede library and style suggestions without weakening P0 safety.

## Identity and architecture

- Project/name/owner / product purpose: TODO
- User journeys, roles, workflows and critical functions: TODO
- Frontend framework/version and renderer: React Vite CSR / Next.js SSR+CSR / Other — TODO
- Router, data fetching, state, forms and TS conventions: TODO
- Backend framework/version and business service boundaries: TODO
- Database/ORM, file storage, queue, Redis and deployment topology: TODO
- API contract/OpenAPI/versioning and clients (web/mobile/BFF): TODO
- Authentication/session/device policy, RBAC/resource scopes, tenant data boundary: TODO
- Sensitive data, retention, required business audit/history and compliance: TODO

## UI / iOS style

- Brand colors and existing semantic tokens: TODO
- Existing CSS/component/icon/font/animation libraries: TODO
- Light/dark themes and density preferences: TODO
- Premium Balanced Glass default or documented alternative: TODO
- Main layout types (dashboard, data workspace, forms, consumer site): TODO
- Target browsers, device classes, localization and accessibility requirements: TODO
- Required visual QA viewport/device/browser tools: TODO

## API, quality and operations

- Per-category AUTH/PUBLIC/AUTHENTICATED/HEAVY/METERED rate policies: TODO
- Proxy trust, multi-instance shared quotas, metered costs and storage limits: TODO
- Pagination default/max, supported cursor/offset, export scope: TODO
- Transaction/idempotency, money/timezone and critical invariants: TODO
- Logging, metrics, trace, alert, retention, backup/restore capabilities: TODO
- Required tests (unit, integration, contract, E2E, security, visual): TODO
- QA environments with access limitations: TODO

## Git, agent autonomy and release policy

- Allowed repo/workspaces, protected branches, target branches: TODO
- Can agent commit? push? merge? to which branches? TODO
- Required CI checks and named reviewers/approval: TODO
- Allowed local/test migrations and forbidden shared/prod operations: TODO
- Release strategy, prod approvals, rollout and recovery/rollback: TODO
- WIP branch policy when required gates fail: TODO

## Overrides / exceptions

Document precise, approved project-specific adjustments. Never bypass P0, claim unknown work passed, assume permission to change production, or copy someone else's fixed rate limit. If a business-critical assumption remains unknown, ask before implementing.
