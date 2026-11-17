# Claim, evidence and committee decision

AI assisted with repository assembly and validation. This work is for education, not investment advice.

## Portfolio pilot decision

I'm holding funding on my Project 2 recommendation until one mandate question is confirmed: does the 8% estimated-return screen apply to the whole funded sleeve, or only to the constrained allocation?

The answer decides the outcome:

- Allocation-level: the constrained allocation passes at 8.31% on the 23-month fit and cleared both locked replay vetoes, so the 25% pilot stands.
- Sleeve-level: the 25/75 pilot (3.49%), the equal-weight fallback (1.88%), and a 50/50 blend (5.09%) all fail the return screen, though all clear the 20% bond floor. A blend would need at least 95.24% in the constrained allocation to pass, which is outside the pilot range.

Expansion toward 50% still requires a genuinely unseen test. The earlier 10.00% equal-weight estimate used the full 59-month window.

**Changed input and result.** Run `python replay.py` after README setup. The fit uses the first 23 monthly returns in place of the full 59. Over the following 36 months, the constrained mix earned 11.34% annualized after costs at 9.45% volatility, versus 15.69% at 9.96% for equal weight. The two locked vetoes were less than 8% net return and volatility at least as high as equal weight. Neither triggered. The proposed blend clears the 20% bond floor at 37.50% and has a training-period return estimate of 3.49%. [Locked prediction and replay](LOCKED_CHANGED_INPUT.md)

**Monitor and reversal.** If funded, compare each month's proposed optimizer weights with the prior proposal. A move greater than 15 percentage points in any fund triggers committee review. A binding mandate failure blocks funding or continued use.

## PAYEMS data decision

**Riskiest claim:** The historical demo uses PAYEMS values available in the selected ALFRED vintage, including only publications allowed by the date convention. Choosing the wrong vintage can introduce look-ahead bias, where a historical decision benefits from information released later.

| Link in the chain | Reviewer evidence |
|---|---|
| Source | Compare the [September 6 vintage](payems_source_vintages/PAYEMS_2024-09-06.csv), the latest captured PAYEMS vintage before October 4, with the [October 4 vintage](payems_source_vintages/PAYEMS_2024-10-04.csv). With an October 4 cutoff, excluding same-day publications leaves August at 158,779 thousand jobs. Including them brings in August's revised 158,851 and September's 159,105. [Captured source index](alfred_download_page.html) |
| Implementation | The [reconstruction](payems_point_in_time.py) derives change events from the captured snapshots and selects the latest eligible value for each observation month. The [rates app](rates_app.py) exposes the date and same-day control. |
| Test | `python payems_verify.py` rebuilds the events from source and asserts both sides of the October 4 boundary. It also checks three fixed values against a separately retrieved November 1 vintage. `python verify_rates_app.py` checks the date rule and exercises the Streamlit controls. [Source notes](evidence/Lab15_PAYEMS_point_in_time_2026_10_27.md) |
| Independent classroom check | `python verify_asof.py` reconciles all 12 planted rows and known signal values. AAA uses 103/101 − 1 = +1.98% as of March 31, compared with +5.83% from the naive data. The fixture checks gate behavior, and its financial-validity checks flag planted prices under the supplied assumptions. [Row-level proof](Lab15_known_answer_provenance_2026_03_31.md) |
| Decision | Approve classroom demonstration within the captured sample. Hold Project 2 admission pending assignment eligibility and evidence for the intended use. [Existing Project 2 review](evidence/Rates_app_Project2_review_2026_10_29.md) |

Captured observations run from August 2024 through September 2026. The snapshots give date-level availability within that capture. Deployment would need decision-time alignment, sufficient sample coverage and evidence that PAYEMS helps the intended decision. The current work does not supply an intraday release audit or predictive validation.

Keep portfolio interpretation separate from the vintage test. Lab 14’s LQD shift from 55% to 80% shows sensitivity to the estimation window under fixed inputs and constraints. Both return estimates are historical. The committee should treat this as scenario evidence and defer any allocation approval requiring full mandate checks.
