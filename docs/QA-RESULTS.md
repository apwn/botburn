# Botburn QA-RESULTS

Package QA for the public **v0.1.0** kit. These checks are **static** against
this repository’s files. They are **not** a live usage-report run and **not**
a claim that all Grok Bot accounts, plans, or report shapes were tested.

Reproduce:

```text
python3 scripts/validate.py
```

## Checks (this package)

| Status | Section | Check | Detail |
| --- | --- | --- | --- |
| see script | required files | README, SKILL, LICENSE, docs, examples, assets, draft notes | present |
| see script | readme | TLDR, install by attaching SKILL.md, v0.1.0, X credit | present |
| see script | skill | usage-review first; managed canvas; TLDR then largest-first charts | present |
| see script | links | all relative markdown/image links | resolve |
| see script | assets | svg + png pair; svg well-formed | present |
| see script | math | sample sums | 44+21+12+9+14=100; 55+43+2=100; 22+51+27=100; 28+16=44 |
| see script | privacy | no private Page URLs, workspace paths, staging chatter | clean |
| see script | claims | no every-account coverage claim; no invented tokens/costs/savings | clean |

The validator prints exact PASS/FAIL lines. Treat that output as the run
record for a given checkout.

Recorded run (this tree):

```text
PASS  required_files
PASS  license_mit
PASS  readme_tldr
PASS  readme_credit
PASS  readme_install
PASS  readme_version
PASS  readme_repo_link
PASS  readme_limitations
PASS  readme_not_just_coding
PASS  readme_deep_dive
PASS  readme_visual
PASS  skill_frontmatter_name
PASS  skill_frontmatter_description
PASS  skill_usage_review_first
PASS  skill_managed_canvas
PASS  skill_tldr_then_charts
PASS  skill_actual_data_only
PASS  description_matches_trigger
PASS  release_notes_draft
PASS  qa_not_all_accounts
PASS  relative_links
PASS  asset_svg
PASS  asset_png
PASS  svg_well_formed
PASS  sample_math
PASS  svg_bar_scale
PASS  privacy_private_canvas_url
PASS  privacy_workspace_path
PASS  privacy_updateskill_chatter
PASS  privacy_draft_skills_path
PASS  privacy_once_hosted
PASS  privacy_all_accounts_tested
PASS  no_invented_costs_or_savings
PASS  lt1_preserved
```

## Limitations (accurate)

- PNG is a raster of the fictional SVG, **not** a live Page screenshot.
- Visual sample is **synthetic**. No live usage-report reads were performed
  for this public package.
- Explore controls (when a real dashboard is later rendered from a user’s
  report) switch embedded views only; they do **not** refresh report data.
- Skill-install body readback was not available during the pre-release kit
  review. That is a tooling limitation, **not** an installation failure.
  Public install is: attach `SKILL.md` to a Grok Bot and ask it to save the
  skill.
- This QA does **not** test every Grok Bot account, plan (weekly /
  Enterprise / trial), or live report schema.
- No tokens, per-call costs, or savings percentages were invented or claimed.
- Rounded `<1%` values in examples are kept as `<1%`.

## Intentionally omitted from this public file

Private audit Page URLs, internal workspace paths, and install-tool process
notes from the pre-release review.
