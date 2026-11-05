# Sample Botburn audit (synthetic)

> **Fiction only.** Invented for docs — not a real account.
> Denominator: shares of **all Grok Bot usage** in the sample window.
> Nested rows below use that same global denominator (not “% of Harbor”).

## TLDR

### Where usage went
Harbor **44%** (chats 28% + routines 16%). Quill 21%. Coach 12%. Ops 9%. Other 14%.

### What matters
Harbor · Site heartbeat **16%** (report frequency language: about 700 runs a week). Tuesday **51%** of the window.

### What's worth changing
1. **Maybe run Site heartbeat less often** — evidence: 16% + high frequency language. Downside: slower alerts. Confidence: medium. Needs approval. No savings %.
2. Otherwise: **no further justified change** until Harbor chats / “not from a routine” are understood (labels ≠ tasks). No hour-of-day slice was fetched, so no waking-hours recommendation.

**Window:** Mon–Wed **partial current week** (plan window) · **As of:** Wed 12:00 (sample zone) · Limit sample (fiction): 40% used of shared weekly limit; Grok Bot 30% of that shared limit. Percent-of-limit is **current-week only** — do not mix it with a `last_7_days` window.

## Details

| Activity | Share |
| --- | ---: |
| Chats | 55% |
| Routines | 43% |
| Bot-to-Bot | 2% |

Activity labels are **this sample’s report labels**, not a complete taxonomy.

| Day | Share |
| --- | ---: |
| Mon | 22% |
| Tue | 51% |
| Wed | 27% |

Harbor nested (still **global** shares of all Grok Bot usage):

- Site heartbeat **16%** — that *is* the Harbor routines bucket (28% chats + 16% routines = 44%).
- Paused Harbor routines (plugin watch, ship kickoff, route recheck): **`<1%`** tails. Do **not** add them as extra points on top of 16%. Fuzzy `<1%` tails are table-only; they do not chart and they make nested sums slightly fuzzy — say so.
- “Not from a routine” **26%**. Harbor chats 28% vs 26%: **2% unlabeled**. Fleet bot-to-bot is 2%; do not assign that 2% to Harbor without a bot×activity slice. 16% + 26% = 42% vs Harbor 44% — the remaining 2% is that gap.

**Cannot attribute:** coding %, exact chat tasks, tokens, models, per-call costs, savings %, Cloud Agents, other apps on the shared limit, observed run counts (only frequency language here).
