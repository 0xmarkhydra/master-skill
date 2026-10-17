---
name: ui-v3-design
description: Build or review a polished iOS-inspired, glass-accented, data-dense, accessible and responsive product UI. Apply to frontend designs, app shells, dashboards, forms and tables; works with Next.js/React and existing stacks without introducing unnecessary libraries.
---

# UI V3 Design — portable visual and interaction standard

Use when implementing, redesigning or auditing UI. This is a **portable visual philosophy**, inspired by a mature enterprise V3 interface, **not** the KPI-BSC application or ASIA branding. Read the repository's own brand tokens and user-approved references first; explicit project requirements win over defaults. For any frontend behavior that touches API, permissions or data, also load `code-logic`.

## 1. Inspect before drawing

1. Discover actual framework, route layout, component library, CSS method, tokens, icon system, responsive constraints, existing screens and user roles. Reuse what is installed. Never migrate a working stack solely to use this skill.
2. Trace the real workflow (actions, forms, permissions, errors, search, pagination). Compare the original screen to the proposed screen so features are not lost.
3. Choose a short visual direction: information hierarchy, surface/tokens, component reuse, state model, keyboard and mobile behavior.
4. Ask for a brand palette only if the project has none and color choice materially affects approval; otherwise use adaptable CSS variables and clearly identify suggested defaults.

## 2. Visual language: modern iOS, restrained glass

- **Look:** calm premium software, clean hierarchy, generous but efficient spacing, softly rounded surfaces, subtle layering and believable depth. Glass is a selective accent for navigation, toolbars, overlays and popovers — not a translucent sheet over every table or form.
- **Theme tokens:** use semantic names (background, foreground, primary, primary-contrast, surface, elevated-surface, muted, border, focus, danger, warning, success). Use project colors, not fixed teal/ASIA or BSC meanings. Support light/dark where project already supports it.
- **Glass:** translucent backgrounds with controlled blur only where it improves navigation; provide an opaque fallback for unsupported browsers, reduced transparency and dense data views. Avoid putting overlays inside ancestors whose transforms/backdrop filters break positioning.
- **Type:** use existing Vietnamese-capable font stack, short labels, readable contrast, clear heading/subheading/body/caption levels. Never shrink text just to make a screenshot fit.
- **Rhythm:** consistent spacing scale (e.g., 4/8/12/16/24/32), radius tiers (e.g., 10/14/18/24), consistent border and shadow intensity. These are examples, not a mandate to overwrite the design system.
- **Icons:** one coherent set. Default to Lucide React when the project already uses or approves it; 16–24px, consistent stroke and purpose. Text labels are mandatory where icon-only meaning is not obvious; icon-only buttons need accessible names.
- **Animation:** short and purposeful; account for `prefers-reduced-motion`. Avoid excessive blur, heavy gradients, bouncy motion, visual noise and inaccessible translucent text.

## 3. One-screen workspace without sacrificing content

- On sufficiently tall **desktop** workspaces, keep header, primary navigation, essential filters/actions and key metrics visible; use meaningful tabs and internal panel/table scrolling for long datasets.
- Do **not** force every website, story, mobile screen, print view or short-height viewport into 100vh. Tablet/mobile and 200% zoom use natural page scrolling, never clipped Save/Approve/Delete.
- Use tabs only for genuine parallel tasks or subdivisions; don't bury major calls to action or unrelated features in artificial tabs. Retain selected filter and page context where appropriate.
- A dense desktop data grid can be wide; constrain scrolling to the grid container instead of causing unintended page-wide horizontal overflow. Sticky columns/headers must not obscure actions or keyboard focus.

## 4. Component rules

**Shell & navigation:** clear active state, adaptable sidebar (expanded/collapsed) and mobile navigation; safe-area insets on supported devices; search and shortcuts reachable without navigation traps.

**Cards & dashboards:** one question per card, real measures with units, time ranges and data freshness. Distinguish zero from unknown; don't fabricate KPIs, trends or fake charts. Show actions and drill-down only if supported by the API and permissions.

**Forms & dialogs:** label every control; show required/optional status, examples/units, inline validation, input preservation on server errors, focused primary action, safe destructive confirmation, duplicate-submission guard and recovery. Ensure dialog focus and Escape work.

**Tables & lists:** search, sorting, filters, reset, counts, server pagination, empty/loading/error states, filter persistence and bounded scrolling. For large GetList never paginate only client-side; defer the API contract to `code-logic`. Exports/prints have their own verified scope, not just current page unless requested.

**Feedback:** present loading only for actual async actions; success only after an API confirms the mutation (or label optimistic UI clearly and roll back on error). Show actionable error/retry and distinguish 401/403/404/409/422/429/network failures.

## 5. Accessibility & performance gates

- Verify at 390px phone, 768px tablet, 1440px desktop, small laptop height and 200% zoom.
- Semantic HTML, keyboard operation, visible focus, readable contrast, 44px-ish touch targets where possible, screen reader labels, reduced motion and localization/long Vietnamese names.
- Do not duplicate CSS overrides or add UI frameworks for decoration. Avoid expensive filters on huge surfaces. Use lazy loading for expensive screens/charts when it measurably helps.

## 6. Deliverable

For each new or changed screen: (a) short visual rationale and reused components, (b) real implementation with all states and API/permission parity, (c) tests and inspected viewports **actually run**, (d) any risks and unverified cases labeled `NOT RUN`. Use `references/SCREEN-REVIEW.md` before marking UI complete. A mockup, screenshot or source inspection **is not live UAT**.
