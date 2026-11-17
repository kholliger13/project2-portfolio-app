# March 31, 2026 — known-answer provenance proof

Source: the student-supplied 12-row classroom table and four ordered rules. Prices are planted training values.

Decision cutoff: March 31, 2026, inclusive. Original row numbers are retained. Exact duplicates compare ticker, month, publication date and price, excluding row number.

| Row | Ticker | Month measured | Published on | Price | Disposition | Reason |
|---:|---|---|---|---:|---|---|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 | admitted | passed all four rules |
| 2 | AAA | 2026-02 | 2026-03-10 | 104.0 | removed | 4: superseded by knowable row 4 |
| 3 | AAA | 2026-03 | 2026-04-10 | 109.0 | removed | 3: published after decision date |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 | admitted | passed all four rules |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 | admitted | passed all four rules |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 | admitted | passed all four rules |
| 7 | BBB | 2026-02 | 2026-03-10 | 97.0 | removed | 2: exact duplicate of row 6 |
| 8 | BBB | 2026-03 | 2026-04-10 | 92.0 | removed | 3: published after decision date |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 | admitted | passed all four rules |
| 10 | CCC | 2026-02 | 2026-04-05 | 112.0 | removed | 3: published after decision date |
| 11 |  | 2026-02 | 2026-03-10 | 99.0 | quarantined | 1: no ticker |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 | admitted | passed all four rules |

**Reconciliation:** 12 source rows = 6 admitted + 5 removed + 1 quarantined. No row disappears from the audit.

## Signal from admitted rows

Return = February price / January price − 1. February is the latest knowable measured month for every ticker.

| Ticker | January row | February row | Calculation | Return |
|---|---:|---:|---|---:|
| AAA | 1 | 4 | 103.0 / 101.0 − 1 | 1.980198% |
| BBB | 5 | 6 | 97.0 / 98.0 − 1 | -1.020408% |
| CCC | 9 | 12 | 111.0 / 110.0 − 1 | 0.909091% |

AAA uses row 4 (103.0), not superseded row 2 (104.0). Using row 2 would produce 2.970297% rather than 1.980198%. The revision reduced the knowable return by 0.990099 percentage points before the decision date.

Rows 3 and 8 describe March but were published April 10. Row 10 describes February but was published April 5. All three came later and must be excluded. A measured month alone does not establish availability.

## V — financial validity, separate from provenance

Yield = 100 / price − 1 under the supplied one-year zero-coupon interpretation.

| Ticker | January yield | February yield |
|---|---:|---:|
| AAA | -0.990099% | -2.912621% |
| BBB | 2.040816% | 3.092784% |
| CCC | -9.090909% | -9.909910% |

Under the exercise’s stated financial checks, AAA and CCC prices above 100 are flagged: their implied yields are negative. The credit-price ordering fails in both months: CCC is priced above AAA and BBB, although the exercise requires AAA > BBB > CCC at equal maturity. These rows pass provenance but fail V. The four provenance rules do not authorize removing them for financial invalidity.

The reported price returns are the assigned signal calculation, not a claim that these planted prices support a valid investment decision.

Verification: all 12 row dispositions and all three returns matched explicitly specified expected results; publication-date equality and ordered duplicate handling also passed. Run `python3 provenance_gate.py` from this folder to reproduce.

This completes the supplied classroom known-answer fixture. PAYEMS is the separate ALFRED application; the bond fixture is not ALFRED market data.
