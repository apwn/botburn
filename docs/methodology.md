# Botburn methodology

## Output shape

1. **TLDR** — Where usage went / What matters / What's worth changing  
2. **Details** — tables, charts, provenance  

Suggestions: at most three, **only if valuable**; else say no justified change. Never high-use=waste. Never invent savings %.

## Each run

1. Load managed `usage-review` via Skill before reads (it wins on conflicts).  
2. Discover live usage-report schema.  
3. Adaptive reads: Source A bot+routine; B activity; C day; deep-dive D/E… as needed.  
4. Global denominator under filters unless the report says otherwise. Nested rows add to the parent; do not double-count `<1%` tails.  
5. Label Sources A/B/C (human-readable).  
6. Default window = current plan period. `last_7_days` only if live schema supports it after an empty reset. Percent-of-limit is current-week only — never mix with a historical slice.  
7. Dashboard / Page / canvas: load managed `canvas` after usage-review; TLDR, then largest-first charts, then embedded drilldowns only for fetched data; source details below. usage-review still wins on report matters.  

## Accuracy

Traceable figures · preserve `<1%` (tables only, not charts) · frequency language ≠ executions · reported money when present · Enterprise/trial wording preserved · activity labels from the report · Page sharing user-controlled.
