---
name: Botburn
description: >-
  When the user asks where Grok Bot usage went, which bots or routines burn the
  most, how to cut usage across all tasks (not only coding), or wants a Botburn
  audit or usage dashboard, run this before answering or changing anything.
---
# Botburn

Community skill **v0.1.0** (early release). Source:
https://github.com/apwn/botburn

Find where Grok Bot usage went across **all** work — chats, routines, bot-to-bot,
and whatever else the report actually labels (group chats, shipping, social,
coaching, ops if present) — not only coding. Do not invent activity buckets
the live schema does not return.

Read-only. Uses the supported usage report only. No invented tokens, models,
dollar estimates, forecasts, or savings. No routine changes, watchers,
publishing, or paid spend without a clear user ask.

If the usage report tool is unavailable, say what Botburn covers without numbers
and point to Settings > Usage & Billing. Stop.

If the report says usage was not checked, do what it says and stop.

Never state a usage figure, price, or reset time the report (or the user) did
not give you.

## Before every audit (mandatory)

1. **Load managed usage-review first.** Call `Skill` with name `usage-review`
   and obey it for reads, wording, denominators, plan/billing language, and
   suggestions. If Botburn and usage-review conflict, **usage-review wins**.
2. **Discover the live schema** for the usage report tool before invoking it.
   Use only dimensions and periods the live schema supports.
3. Then follow the accuracy gate and flow below.

## Two-layer output (required — keep it simple)

Always answer in **plain language**. Prefer short words. No jargon wall.

### Layer 1 — TLDR (always first)

Open with a short **TLDR** the user can act on in seconds:

1. **Where usage went** — biggest consumer (bot and/or routine) with its reported
   share.
2. **What matters** — one key finding (for example a day spike or a frequent
   check), still from the report.
3. **What's worth changing** — one suggested next step **only if** evidence
   supports a change; otherwise say clearly **no justified change right now**.
   If you suggest a change: what would change, why (tied to a reported share),
   downside, confidence (high/medium/low). **Never** call high use “waste.”
   **Never** invent a savings %.
4. Put **window** and **denominator** next to the TLDR (or immediately under it).

In chat: TLDR can be the whole reply for a quick ask. On a Page: TLDR section
at the top; everything else below.

### Layer 2 — Details (below, not dominating)

Only after the TLDR: charts/tables, drilldowns, provenance (Sources A/B/C…),
gaps, and “what cannot be attributed.” Details support the TLDR; they must not
bury it.

## Core structure (chat and Page)

Use these three plain headings (or equivalent clear labels):

1. **Where usage went**
2. **What matters**
3. **What's worth changing**

Then optional **Details** (provenance, full tables, deep-dive).

## Accuracy gate (non-negotiable)

1. **Traceability.** Every figure: as-of (user zone), period/window, denominator
   (“shares of all Grok Bot usage in that period” unless the report says
   otherwise). Label slices **Source A / B / C** (human-readable) — never
   internal tool/message ids.
2. **Preserve rounding.** Keep `<1%`. Do not chart `<1%` as 0, 0.5, or 1 — tables
   only.
3. **Separate reads ≠ one instant.** Max two dimensions per request. If
   headlines differ across Sources, say so; do not fake one timestamp. Matching
   headlines may be noted.
4. **No blending snapshots.** New audit replaces the prior embedded snapshot.
5. **Frequency language ≠ observed executions.** “About N runs a week” is report
   frequency language only.
6. **Labels ≠ exact tasks.** “Chats”, “Not from a routine”, bot names do not
   prove what was done.
7. **High share ≠ waste.** Observation vs hypothesis. Changes need approval.
8. **No fabrication; copy reported money.** Invented dollars/savings forbidden.
   Reproduce on-demand amounts exactly when the report shows them.
9. **Listing limits.** Prefer a high bot/routine list limit; disclose “Other”
   aggregation.
10. **Partial windows.** Say when the week is partial; day shares use that
    window’s denominator.
11. **Gaps first-class.** Mark gaps, hypotheses, coverage limits.
12. **Reconciliation.** Nested rows add to the parent per the report, using
    the **global** denominator unless the report renormalized (say if it
    did). Do not add `<1%` tails as extra integer points on top of a parent
    that already accounts for them. Fuzzy `<1%` tails — say so. Gaps
    (child sums short of parent) stay gaps — not tokens or coding %.
13. **Plan shape from the report.** Weekly limit, Enterprise team usage, or
    trial — do not force the wrong template. Enterprise remaining usage → team
    admin. usage-review wins on plan/billing language.

## Hard rules

1. Load and obey usage-review before any usage reads. Accuracy gate always on.
2. After schema discovery, ≤2 dimensions per request; only live-supported ones.
3. Use the report’s own labels. Never name tools/options/skill ids/folders/tokens
   to the user.
4. No invented tokens/models/per-call costs/estimated dollars/future run counts.
   Reproduce reported money when present. Schedules in words only.
5. Shares are of **all Grok Bot usage** in the period unless the report says
   otherwise. Filtered bot reads keep that global denominator unless the report
   renormalizes (say if it does).
6. At most **three** change suggestions, and **only if valuable**. If none are
   justified, say **no justified change** and stop suggesting. Each suggestion:
   what / why (evidence) / downside / confidence / approval required.
7. No recurring usage watcher. Offer one reminder at reset if asked.
8. Adaptive, minimal reads.

## Default audit flow

### 1. Snapshot — Source A

No-arg read for “how much left / when reset.”

For an audit: bot + routine for the default current period (often this week).
Match plan shape (weekly / Enterprise / trial). Recent empty reset →
`last_7_days` when supported; say percent-of-limit is current-week only when the
report shows one.

### 2. All-task slices when needed

- Activity → **Source B**
- Day → **Source C**

Skip if Source A already answers.

### 3. Rare transcript peek

At most two small peeks if a name is opaque. Inferences = hypothesis.

### 4. Report (TLDR first)

Lead with TLDR using Where / What matters / What's worth changing, then details
if needed.

### 5. Suggest only if valuable, then wait

Suggestion shapes (usage-review family): less often; waking hours; schedule →
trigger; merge overlaps; stop in-flight + pause feeders; on-demand off / spend
limit when shown.

Never change built-in check-ins. Ask which to make; change only after yes.
Pause rather than delete. Other bots’ routines: user edits that bot’s list.

## Deep-dive mode

When they want more detail, adaptively add (do not explode every cross-product):

1. Fleet **bot + activity** (Source D)
2. High list limit for full routines on Source A
3. Largest bot(s): **bot + day**; optional activity + day
4. ≤2 transcript peeks if needed

Qualitative tags from routine names/samples only — **never** invent a coding %
or assign a whole bot’s share to coding.

Always include **what cannot be attributed**: coding %, tasks inside chats,
tokens/models, Cloud Agents (https://cursor.com/dashboard?tab=usage), other apps
on a shared limit, observed run counts when only frequency language exists.


## Visual dashboard (when asked for a Page / dashboard / canvas)

When the user wants a **dashboard**, **visual audit**, **Page**, or **canvas**
(not a quick chat TLDR-only answer):

1. **Load managed canvas.** Call `Skill` with name `canvas` and obey it for
   Page/canvas rendering, kit components, and write rules.
2. **usage-review still wins** on usage reads, wording, denominators,
   plan/billing language, and suggestions. It is loaded first (see Before
   every audit). If canvas and usage-review conflict on report matters,
   **usage-review wins**.
3. After the usage reads, render a **managed canvas** in this order:
   1. **TLDR** at top (Where / What matters / What's worth changing + window +
      denominator).
   2. **Largest-first charts** — bot bars, then activity composition, then day
      trend. Chart **only slices you actually fetched**.
   3. **Embedded view drilldowns** only when that view has **actual data**
      from this pass (for example largest-bot day, top routines). Explore
      controls (`Segmented` / `Select`) switch those views. Controls change
      what is shown only — **no pretend live refresh**.
   4. **Source details below** — full tables, provenance (Sources A/B/C…),
      and cannot-attribute (collapsible when helpful).

Use kit charts (`Bars`, `Columns`, `Pie`, …). Preserve `<1%` in tables only.
Do **not** force a canvas for a quick verbal ask — chat TLDR is enough.

### Managed canvas rules

- Accuracy first; simple language; user-owned write-up (not an official
  product UI).
- Embed only this pass’s figures; Source A/B/C…; window; denominator.
- `<1%` table-only; frequency language labeled correctly.
- Charts and drilldown views only for numeric shares actually gathered.
  Omit empty chart frames and placeholder views.
- No fake refresh. Repeat audits update the same canvas/Page.
- Page sharing is **user-controlled**. Claim private only after verifying
  sharing (e.g. library listing).
- Chat with a canvas: one or two lines + link — do not dump the Page into
  chat.

Quick verbal ask → chat TLDR only is fine.

## Privacy

Do not paste real audits into public README/examples. Synthetic examples only
in the public package.

## Out of scope

- Token profilers, invented dollar forecasts
- Auto routine edits / recurring Botburn watchers
- Publishing / repos / paid research without an explicit ask
- Affiliation with xAI, Grok, or Cursor
- Assuming ordinary Cursor IDE access equals Grok Bot usage reporting
