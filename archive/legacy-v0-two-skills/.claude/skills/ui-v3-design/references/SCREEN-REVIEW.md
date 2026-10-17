# UI V3 screen review checklist

**Identity:** Reuse product brand tokens; preserve approved copy, routes, actions, roles and component conventions. The V3 aesthetic is a reusable *design direction*, not a requirement to retain ASIA colors or KPI-specific screens.

**Desktop:** navigation clear; page title, important KPIs/actions and filters findable; useful tabs only; grid scroll confined; no unnecessary main-document horizontal scroll; appropriate 1440px and short-height viewport behavior.

**Tablet/mobile/zoom:** 768px, 390px and 200% browser zoom; no clipped primary/destructive actions, no overlays obscuring forms, natural body scrolling when needed, readable typography and safe-area compatibility.

**States:** initial, real loading, empty, error/retry, unauthorized, 429 with retry guidance, optimistic mutation rollback if used, field validation, confirmation, success only after persistence, long translations/names, large row counts and no-data-vs-zero.

**Accessibility:** semantic headings; labels; aria-current on page navigation; focus visibility and logical keyboard tab order; dialogs with focus restore; no icon-only unlabeled actions; meaningful status text beyond color; reduced-motion and sufficient contrast.

**Data truth:** no fabricated KPI, customer, company or permissions; no client-side role spoofing; list pagination backed by actual server contract; exports and print verify full authorized scope where applicable.

**Performance:** avoid uncontrolled blur layers, expensive animations and repeated network calls; respect current stack's cache and query libraries. No new dependency without clear benefit.

**Verification record:** Mark each as PASS / FAIL / NOT RUN with the actual evidence: code inspection, runtime desktop/tablet/mobile, keyboard, zoom, critical workflow, browser console/network and authorized API behavior. If no browser is available, state NOT RUN; a static fixture is not production UAT.
