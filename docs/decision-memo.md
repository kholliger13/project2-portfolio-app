# Claim, evidence and committee decision

I used OpenAI Codex to implement, test and document the app and replay, and Claude
(Anthropic) to review my plan, draft two predictions at my request (the 23/36 replay and
the 50 bp cost check), and run one cold run. I wrote the Locked Changed-Input Record
prediction (24-month window) myself, without AI. The analysis and the decision are mine.
Education, not investment advice.

## Portfolio pilot decision

Pilot. Allocate 25% of the Diversified Growth sleeve to the constrained process and 75%
to equal weight, rebalanced monthly to fixed targets. Range 25–50%: expand toward 50% only
after six months of live results clear the same two vetoes used in the replay. The funded
sleeve holds at least 38.8% in LQD and TLT and has lower estimated volatility than equal
weight in all three windows.

Professor's guidance, Nov 19, 2026: the 8% screen may apply to either the funded sleeve
or the constrained allocation; if the sleeve fails, test the constrained allocation. No
estimation window is perfectly current or perfectly historical. I apply the screen to the
funded sleeve on estimates available at the decision date and report the replay as
historical evidence. The pilot passes both ways: the 25/75 sleeve estimates 9.58% (all
59 months; 13.47% with 36, 12.70% with 24), and the constrained allocation alone passed
on the 2021–2023 training estimates (8.31%), where the sleeve estimated 3.49%.

**Triggers (any one returns the pilot to the committee):**

1. Any fund's newly proposed weight moves more than 15 points from the prior month's proposal.
2. The point-in-time PAYEMS change is negative for two consecutive months.
3. At a monthly re-estimate, the funded sleeve's estimated return falls below 8% or LQD + TLT falls below 20%.
4. After six months, the constrained portion's realized net return is below 8% annualized,
   or its realized volatility is at least equal weight's.

**Reversal:** if trigger 3 or 4 fires, revert to 100% equal weight, if equal weight passes the
mandate at that re-estimate, and reject the process.

**Changed input and result.** Run `python replay.py` after README setup. The fit uses the first 23 monthly returns in place of the full 59. Over the following 36 months, the constrained mix earned 11.34% annualized after costs at 9.45% volatility, versus 15.69% at 9.96% for equal weight. The two locked vetoes were less than 8% net return and volatility at least as high as equal weight. Neither triggered. The proposed blend clears the 20% bond floor at 37.50% and has a training-period return estimate of 3.49%. [Locked prediction and replay](../LOCKED_CHANGED_INPUT.md)

## PAYEMS data decision

**November 19, 2026 decision.** Admit PAYEMS as the Project 2 point-in-time signal, for monitoring only. The Project 2 instructions require one point-in-time signal and set no restriction on series type, which resolves the earlier eligibility hold. The signal is the change in nonfarm payrolls between the two latest months, using only the ALFRED vintage available the day before each decision (same-day releases excluded). It does not set portfolio weights. Its coverage (Aug 2024–Sep 2026) is too short to test predictive value, so it serves as a committee review trigger, not an allocation input. Two consecutive negative months are required, because PAYEMS is revised for two months after release and a single negative reading is often reversed. [Project 2 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-2-investment-management-application.md) · [PAYEMS data card](../evidence/PAYEMS_data_card_2026_10_29.md)

The latest captured payroll change is **+29 thousand jobs** (159,044 in September minus 159,015 in August). The October 2, 2026 vintage is eligible starting October 3 under the previous-day rule. The positive reading does not trigger committee review. [Captured October 2 vintage](../payems_source_vintages/PAYEMS_2026-10-02.csv)

**Riskiest claim:** The historical demo uses PAYEMS values available in the selected ALFRED vintage, including only publications allowed by the date convention. Choosing the wrong vintage can introduce look-ahead bias, where a historical decision benefits from information released later.

| Link in the chain | Reviewer evidence |
|---|---|
| Source | Compare the [September 6 vintage](../payems_source_vintages/PAYEMS_2024-09-06.csv), the latest captured PAYEMS vintage before October 4, with the [October 4 vintage](../payems_source_vintages/PAYEMS_2024-10-04.csv). With an October 4 cutoff, excluding same-day publications leaves August at 158,779 thousand jobs. Including them brings in August's revised 158,851 and September's 159,105. [Captured source index](../alfred_download_page.html) |
| Implementation | The [reconstruction](../payems_point_in_time.py) derives change events from the captured snapshots and selects the latest eligible value for each observation month. The [rates app](../rates_app.py) exposes the date and same-day control. |
| Test | `python payems_verify.py` rebuilds the events from source and asserts both sides of the October 4 boundary. It also checks three fixed values against a separately retrieved November 1 vintage. `python verify_rates_app.py` checks the date rule and exercises the Streamlit controls. [Source notes](../evidence/Lab15_PAYEMS_point_in_time_2026_10_27.md) |
| Independent classroom check | `python verify_asof.py` reconciles all 12 planted rows and known signal values. AAA uses 103/101 − 1 = +1.98% as of March 31, compared with +5.83% from the naive data. The fixture checks gate behavior, and its financial-validity checks flag planted prices under the supplied assumptions. [Row-level proof](../Lab15_known_answer_provenance_2026_03_31.md) |
| Decision | Admit for monitoring within the captured sample. The prior eligibility hold is superseded. [Earlier Project 2 review](../evidence/Rates_app_Project2_review_2026_10_29.md) |

Captured observations run from August 2024 through September 2026. The sample is too short to test predictive value, and the vintages establish date-level availability. An unavailable reading or a decision outside the capture yields no monitoring signal.

Keep portfolio interpretation separate from the vintage test. Lab 14’s LQD shift from 55% to 80% shows sensitivity to the estimation window under fixed inputs and constraints. Both return estimates are historical. The committee should treat this as scenario evidence and defer any allocation approval requiring full mandate checks.
