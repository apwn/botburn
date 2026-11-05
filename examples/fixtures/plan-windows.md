# Scenario fixture: current plan window vs historical (synthetic)

Fiction only. Not a live read.

- Default audit window = **current plan period** (here a partial week Mon–Wed).
- **Percent-of-limit** (sample: 40% used / Grok Bot 30%) is **current-week only**.
- Do not quote that percent-of-limit against a `last_7_days` slice.
- After an empty reset, `last_7_days` only if the **live schema** supports it — then say the historical slice is not the current plan week.
- Day shares (22 / 51 / 27) use the **fetched window’s** denominator, not a full week invented from three days.
