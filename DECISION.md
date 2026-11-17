# Claim, evidence and committee decision

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
