# Sample Botburn audit (synthetic)

> **Fiction only.** Invented for docs — not a real account.
> Denominator: shares of **all Grok Bot usage** in the sample window.

## TLDR

### Where usage went
Harbor **44%** (chats 28% + routines 16%). Quill 21%. Coach 12%. Ops 9%. Other 14%.

### What matters
Harbor · Site heartbeat **16%** (report frequency language: about 700 runs a week). Wednesday **51%** of the window.

### What's worth changing
1. **Maybe run Site heartbeat less often** — evidence: 16% + high frequency language. Downside: slower alerts. Confidence: medium. Needs approval. No savings %.
2. If overnight Ops pulses go unread: waking-hours only. Downside: overnight failures wait. Confidence: medium. Needs approval.
3. Otherwise: **no further justified change** until Harbor chats / “not from a routine” are understood (labels ≠ tasks).

**Window:** Mon–Wed partial week · **As of:** Wed 12:00 America/Costa_Rica · Limit sample: 31% used (shared); Grok Bot 27%.

## Details

| Activity | Share |
| --- | ---: |
| Chats | 55% |
| Routines | 43% |
| Bot-to-Bot | 2% |

| Day | Share |
| --- | ---: |
| Mon | 22% |
| Tue | 51% |
| Wed | 27% |

Harbor routines (global shares): heartbeat 16% · plugin watch 1% · ship kickoff 1% paused · route recheck `<1%` paused · not from a routine 26%.

**Cannot attribute:** coding %, exact chat tasks, tokens, Cloud Agents, other apps on shared limit.
