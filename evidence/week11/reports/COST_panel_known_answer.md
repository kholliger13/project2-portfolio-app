# COST panel — known-answer verification

Source: saved SEC companyfacts snapshot, as of 2026-11-03. Expected values supplied by the user; actual values calculated independently from selected SEC facts.

| Fiscal-year-end | R&D / revenue | Liabilities | Equity | Liabilities / equity | Expected | Match |
|---|---|---:|---:|---:|---:|---|
| 2022-08-28 | not found | 43,519,000,000 | 20,642,000,000 | 2.11 | 2.11 | pass |
| 2023-09-03 | not found | 43,936,000,000 | 25,058,000,000 | 1.75 | 1.75 | pass |
| 2024-09-01 | not found | 46,209,000,000 | 23,622,000,000 | 1.96 | 1.96 | pass |
| 2025-08-31 | not found | 47,935,000,000 | 29,164,000,000 | 1.64 | 1.64 | pass |
| 2026-08-30 | not found | 53,242,000,000 | 35,803,000,000 | 1.49 | 1.49 | pass |

Revenue annual growth = (($303,154,000,000 / $226,954,000,000)^(1/4) − 1) × 100 = **7.51%** — matches.

R&D ratios are not found because the required R&D fact is missing; the R&D threshold check is not known, never fail or zero.

Panel checks: Buffett pass / pass / pass; Cathie Wood pass / not known (revised growth threshold: 5%); Burry pass / pass. The latest-year liabilities test passes despite the earliest-year ratio exceeding the ceiling, because the rule applies only to the latest year.

Verified in Streamlit AppTest: seven check rows, three side-by-side memo columns, all three verdicts, displayed growth and latest leverage. All saved memos pass the unprinted-number checker and match the shared report hash.
