# CodeLocal Skills × Ponytail — skill-only integration

**Brand:** CodeLocal Skills. **Upstream:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail). **Mode for coding tasks:** Ultra by default under this project's AGENTS.md/CLAUDE.md. This is a **static Agent Skill installation**, not a Codex/Claude plugin and **has no lifecycle hooks or background process**.

## Specialist skills versus complementary skills

| Active skill | Ownership | Collaboration with Ponytail |
| --- | --- | --- |
| `backend-engineering` | Server authority, API contracts, DB, transaction, audit, security, delivery | Ponytail can remove speculative layers/unused dependencies, **cannot** remove P0 controls or tests |
| `react-frontend-engineering` | React state, API UX, forms, routing, feature parity | Reuse existing hooks/components and platform features without fake parity or mock APIs |
| `ios-inspired-ui-design` | Premium Balanced Glass, adaptive density, tokens, visual QA | Prefer existing design system/CSS, without reducing accessibility, responsive or visual QA |
| `ponytail` | Minimal complete implementation / Ultra challenge | Cross-cutting advisor, not a domain authority |
| `ponytail-review` | Read-only diff review | Findings require concrete reproductions, P0/P1 prioritize |
| `ponytail-audit` | Read-only repo audit | Audit product/code paths and report any unreviewed scope |
| `ponytail-debt` | Read-only shortcut markers | Identify ceiling and upgrade trigger; no silent debt forgiveness |
| `ponytail-gain` | **Upstream benchmarks only** | Never claim measured savings for this repository |
| `ponytail-help` | Upstream command reference | Repo-specific activation rules below override plugin-only instructions |

## Decision precedence: safety and accepted scope above terseness

1. Follow user's concrete, approved scope, platform and destination project's existing conventions, plus P0 auth/data/contract/feature safety.
2. The three domain skills own **correctness and Definition of Done** for their areas. A necessary feature, error check, rollback, approval flow, accessibility behavior or test is never 'over-engineering'.
3. After understanding the task and tracing impacted consumers, apply Ponytail's ladder: do we need the extra code? → reuse project code → standard library → native platform → existing dependency → minimal readable solution.
4. **Ultra** may flag unnecessary parts *before* implementation and suggest simpler alternatives. It must not silently ignore explicit requirements or stall an authorized task; ask only when a material scope/risk ambiguity blocks safe implementation. If the user explicitly approved a large migration or an entire capability, finish it and simplify **how**, not **whether**, it is done.
5. Shortcut markers `shortcut: <limit>, <upgrade trigger>` document genuine contextual limits, not hidden permission to postpone P0.
6. In completion reports include evidence for PASS/FAIL/NOT RUN/BLOCKED and separate Git commit/push/merge/CI/deploy. Ponytail's preferred short reply cannot suppress significant risks or unrun checks.

## Trigger and mode behavior

- On writing, fixing or refactoring code: read `ponytail/SKILL.md` and use its **ultra** decision policy alongside relevant engineering skills. `ultra` here is a *documented agent instruction*, **not** a hook-provided switch or a persisted global setting.
- For a diff review: use `ponytail-review`; full repo audit: `ponytail-audit`; debt ledger: `ponytail-debt`; upstream figures: `ponytail-gain`; usage: `ponytail-help`. Do not auto-run read-only audits against every task.
- To opt out for the current user request, honor "Ponytail off" or "normal mode" while continuing mandatory CodeLocal domain rules. To request lighter guidance, use "Ponytail lite/full". Avoid claiming agent-wide persistent state without a real host configuration.
- Codex skill selection varies by client. Explicit prompts like "Use `ponytail` in ultra mode with `backend-engineering`" are portable. Do **not** tell users plugin-only slash commands, environment hooks or auto-start are installed.
- This kit is not a repository-wide install in every CodeLocal application. To use it elsewhere, copy the skills and **merge** relevant `AGENTS.md` policy into that project. Do not overwrite its existing instructions.

## Documentation and attribution

Six upstream files are kept as authored under `skills/ponytail*/SKILL.md`; brand-specific policy is kept **outside** their copyrighted bodies, under this document and the project policies. The six canonical copies are synchronized to both `.agents/skills/` and `.claude/skills/`. See `third_party/ponytail/SOURCE.md` and MIT LICENSE. Third-party attribution must remain visible; do not imply CodeLocal authored Ponytail.

### Before releasing an integration change

Run `python3 tools/verify_kit.py` and `python3 -m unittest discover -s tools -p 'test_*.py' -v`. Check the source+mirror sets, MIT attribution, rulebook counts for three domain skills, and lack of plugin hooks. A passing Markdown consistency test does **not** prove runtime behavior inside Codex or Claude.
