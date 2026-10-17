# CodeLocal Skills — AI agent operating rules (v1.1)

Applies to repositories adopting this portable kit. AGENTS.md and CLAUDE.md in this kit must be byte-identical. Higher-priority platform instructions, user requests and existing repository-specific policies prevail when compatible with P0 safety. Do not silently overwrite downstream policies.

## 1. Dispatch exactly the relevant specialists

- **backend-engineering** — API, server-authoritative business rules, database, migrations, auth/authZ, rate limiting, audit, observability, testing, releases and Git safety. Read skills/backend-engineering/SKILL.md and task-relevant references.
- **react-frontend-engineering** — React behavior, components, server/UI/URL/form state, typed API integration, sessions, forms, tables, routes, accessibility interactions, test coverage and migration parity. Read skills/react-frontend-engineering/SKILL.md and relevant references.
- **ios-inspired-ui-design** — semantic design system, premium balanced glass, adaptive density, layout, responsive, typography, icons, motion, visual a11y and QA. Read skills/ios-inspired-ui-design/SKILL.md and relevant references.
- **ponytail (Ultra mode)** — apply to implementation/refactoring after understanding the real task: minimize new code by reusing what exists, **never** remove required P0/P1 checks or already-approved features. Ultra may question speculative extra scope but must not veto user-approved work. Read `skills/ponytail/SKILL.md` and `docs/PONYTAIL-INTEGRATION.md`.
- **ponytail-review** — read-only review of a diff; **ponytail-audit** — read-only review of a repo; **ponytail-debt** — read-only shortcut ledger; **ponytail-gain** — upstream benchmark (not project measurements); **ponytail-help** — Ponytail reference. Load these only on corresponding requests, not unconditionally.
- Six Ponytail skills are MIT-licensed third-party material from DietrichGebert/ponytail; see `third_party/ponytail/LICENSE` and `SOURCE.md`. CodeLocal Skills is the curated kit's brand and does not claim authorship of Ponytail.
- Combine skills when the task crosses boundaries (e.g. React CRUD + backend pagination + design). Never let frontend visual choices override backend permissions or business authority.
- When running in Codex or Claude and their mirrored directories are installed, load corresponding local mirrored skill. Canonical source is skills/<name>/; both mirrors must remain byte-for-byte equivalent.
- Read templates/PROJECT-PROFILE.md (if completed) and actual repository instructions, branches, installed tools, contracts and existing components **before** choosing a stack. No hardcoded KPI-BSC branding, default branch, framework, env or quota.

## 2. Global P0 constraints

1. Preserve staged, unstaged, untracked and other-agent work; no destructive reset, force push, silent conflict overwrite or unauthorized release.
2. Server-side authorization and scoped data access are mandatory. Never use hidden UI elements as security. Validate user input, protect SQL, secrets and client-visible sensitive fields.
3. Preserve established API contracts, business logic, data and routes without an authorized migration/versioning and compatibility plan.
4. Do not disable authentication, permission checks, rate limits, input validation or tests to make an error disappear.
5. No fake API success, mock production fallback, fabricated KPI or claim of test/remote success without evidence.
6. Never auto-operate destructively against shared/prod DB/infrastructure; obtain authorization and an appropriate recovery plan.
7. Feature parity before replacement; styling must not hide or remove critical actions.
8. Keep implementation lean; use project libraries and conventions first, optional tools only where justified. CodeLocal safety, business correctness, feature parity, tests, and user-approved scope are never negotiable for Ponytail terseness.

## 3. Smart Production Standard and Risk-based Quality Gate

- **P0**: correctness, authorization, data safety, contract and feature integrity, truthful evidence.
- **P1**: maintainability, complete error/async UX, suitable tests, observability, responsive/accessibility.
- **P2**: contextual performance, cache/queue/distributed tracing, sophisticated effects and animation.
- Identify Low/Medium/High/Critical risk. Run checks relevant to change: static checks, test, security, contract, browser visual/interaction, data migration verification as applicable.
- PASS = executed+passed; FAIL = executed+failed; NOT RUN = not executed; BLOCKED = prerequisite/permission missing. Do not infer PASS from source alone or from mock fixtures.
- Required FAIL, high-risk NOT RUN/BLOCKED or known P0 block automatic merge/deploy. Safe WIP storage on explicitly authorized branches may continue. Project-aware auto delivery authorizes Git actions only under actual project policy and permissions; production requires release gate.

## 4. Completion and delivery evidence

Report changed scope/files, feature and API behavior, security/data/compatibility considerations, exact verification result and residual risk. Distinguish *edited*, *tested*, *committed*, *pushed*, *merged*, *CI*, *deployed* and *live UAT* independently. State unverified items explicitly.

When updating this kit, run: python3 tools/verify_kit.py, python3 -m unittest discover -s tools -p 'test_*.py' -v and cmp -s AGENTS.md CLAUDE.md. Keep **all nine** skill mirrors in lockstep; check the old legacy kit is not active and preserve third-party attribution.