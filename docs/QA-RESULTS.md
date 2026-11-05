# Botburn QA-RESULTS

Package QA for the public **v0.1.0** kit.

This file separates **executed** checks from **untested** live runtime.
Nothing here is a live usage-report run or a claim that all Grok Bot accounts, plans, or report shapes were tested.

Reproduce:

```text
python3 scripts/validate.py
python3 scripts/validate.py --selftest
```

## Executed (this checkout)

### Static kit validator — all PASS

`python3 scripts/validate.py` on this tree: **all checks passed**.

Required files, MIT, README (TLDR / credit / install / version / repo /
limitations / all-task value / deep dive / visual / windows / nested denom),
SKILL (frontmatter, usage-review first, managed canvas, TLDR then charts,
actual-data drilldowns, live schema discover), description trigger, draft
release notes, relative links, SVG well-formed 960×750, PNG 960×750 matching
SVG, sample math (44+21+12+9+14; 55+43+2; 22+51+27; 28+16=44), SVG bar scale
largest-first, days title not overlapping columns, Tue 51% TLDR vs table,
Harbor nested recon (heartbeat = routines parent; `<1%` tails; 2% gap
disclosed), scenario fixtures, privacy (no canvas URL / workspace path /
email / staging chatter), no phantom token/coding/cost/savings telemetry,
`<1%` preserved and not charted, sample recommendations (heartbeat only).

### Negative fixtures — SELFTEST PASS

`python3 scripts/validate.py --selftest` (8 mutations, each must FAIL):

1. missing `SKILL.md` → `required_files`
2. broken `./nope.md` → `relative_links`
3. Quill 20% → `sample_math`
4. private canvas Page URL → `privacy_private_canvas_url`
5. invented token counts / coding share / savings share → `no_phantom_telemetry`
6. Wednesday 51% vs Tue table → `sample_day_consistency`
7. paused tails `1%` on 16% parent → `sample_nested_recon`
8. days title moved into Tue column → `svg_days_title_clear`

### Visual assets (human + geometry)

- SVG/PNG inspected: days title fully readable; Tue 51% bar no longer clips
  it; Mon/Tue/Wed labels visible; bot bars largest-first on a shared 0–100%
  scale; activity bars same scale; insight box clear of columns.
- PNG is a **raster of the fictional SVG**, not a live Page screenshot.
  Regenerated at 960×750 after the layout fix.

### Public links (HTTP from this environment)

| URL | Result |
| --- | --- |
| https://github.com/apwn/botburn | 200 |
| https://x.com/ThomasKanze | 200 (HEAD); some fetchers 403 (X bot wall) |
| https://cursor.com/dashboard?tab=usage | 403 / auth redirect — expected, not a 404 |

Relative markdown/image links: validator `relative_links` PASS.

## Not executed / untestable here

- Live Grok Bot usage-report reads (any account, plan, or schema).
- Installed-skill save/sync (`@Botburn` after attach-and-save).
- Managed `usage-review` / managed `canvas` runtime against a real Page.
- Cross-account compatibility (weekly / Enterprise / trial).
- Whether the live schema still names `last_7_days` or any given dimension.
- Real nested/filter renormalization behavior beyond what the skill *instructs*.

Do not treat the static PASS list as a runtime pass.

## Material defects found in PR #1 and fixed in this update

| Sev | Finding | Fix |
| --- | --- | --- |
| High | Sample TLDR said Wednesday 51%; table/SVG/README said Tuesday | TLDR → Tuesday |
| High | Harbor nested 16%+1%+1%+26%+`<1%` double-counted vs 44% = 28+16 | Heartbeat 16% = routines parent; paused tails `<1%`; 2% gap disclosed |
| High | SVG/PNG: “Days in window (shared baseline)” clipped by Tue 51% bar | Taller canvas; columns moved down; PNG regenerated 960×750 |
| Med | Unevidenced “overnight Ops / waking-hours” recommendation (no hour slice) | Removed; only heartbeat suggestion |
| Med | 31% used / Grok Bot 27% looked like leaked account figures | Replaced with round fictional 40% / 30%, labeled fiction |
| Med | README omitted current-week vs `last_7_days` and nested/filter denom | Added limitation bullets |
| Med | Validator was positive-regex only (would not catch the bugs above) | Behavioral checks + 8 negative fixtures |
| Low | `America/Costa_Rica` as-of looked like a private audit stamp | “sample zone” |

## Residual limitations

- PNG fonts are a SVG raster (not Grok Bot kit chrome).
- Explore controls, when later used on a real dashboard, switch views only;
  they do not refresh report data.
- Skill-install body readback is still untestable here. Public install remains:
  attach `SKILL.md` to a Grok Bot and ask it to save the skill.
- No tokens, per-call costs, savings %, or coding % are claimed.
- Rounded `<1%` stays `<1%` and is not charted.

## Intentionally omitted

Private audit Page URLs, internal workspace paths, and install-tool process
notes from the pre-release review.
