# Botburn QA checklist

Requirements to verify — **not** a claim that all were runtime-tested, and
**not** a claim that all Grok Bot accounts were tested.

```text
python3 scripts/validate.py
python3 scripts/validate.py --selftest
```

## Display
- [ ] TLDR first: Where usage went / What matters / What's worth changing
- [ ] Window + denominator near TLDR
- [ ] Details below, not burying summary
- [ ] ≤3 suggestions only if valuable; else “no justified change”
- [ ] No high-use=waste; no invented savings; no rec without a fetched slice
- [ ] Dashboard: managed canvas; largest-first charts; drilldowns only with actual data

## Accuracy
- [ ] Nested/filtered shares stay global unless the report renormalizes
- [ ] Nested children add to parent; `<1%` tails not extra integer points
- [ ] Current plan window vs `last_7_days`; percent-of-limit is current-week only
- [ ] Day TLDR names the max day in the table
- [ ] `<1%` table-only, not charted as 0 / 0.5 / 1

## Package
- [ ] SKILL frontmatter name + description
- [ ] usage-review first; usage-review wins on report conflicts
- [ ] README sells all-task value; synthetic visual; deep dive; X credit
- [ ] Install: attach SKILL.md to a Grok Bot and ask to save
- [ ] v0.1.0 early-release note; draft release notes (unpublished)
- [ ] Assistant-assisted install; Cursor ≠ Grok usage access
- [ ] Privacy scan clean (no private Page URLs, workspace paths, leftover staging-host language)
- [ ] Relative links and SVG/PNG resolve; sample math identities hold
- [ ] Negative selftest catches broken links, bad math, double-count, clip, phantom telemetry
