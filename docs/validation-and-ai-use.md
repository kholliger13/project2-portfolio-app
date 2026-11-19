# Validation and AI use

**AI use.** I used OpenAI Codex to implement, test and document the app, the replay and this repository. I used Claude (Anthropic) to review my plan, draft the replay prediction and the 50 bp cost prediction at my request, and run one independent cold run of the README. **The analysis and the decision are mine.** This is education, not investment advice.

[Project 2 repository](https://github.com/kholliger13/project2-portfolio-app)

## 1. What was checked

Run the automated checks and replay with `sh review.sh && python replay.py` from a clean checkout after the [README setup](https://github.com/kholliger13/project2-portfolio-app#run-from-a-clean-checkout). Any failure stops the run. The independent recalculation and additional stress cases are documented separately below.

| Check | How | Result |
|---|---|---|
| Baseline math | [Baseline script](https://github.com/kholliger13/project2-portfolio-app/blob/main/lab13_baselines.py) reproduces the Meridian benchmark, equal weight and inverse volatility | Matches the saved Meridian baseline record |
| Portfolio app | [Portfolio app verification](https://github.com/kholliger13/project2-portfolio-app/blob/main/verify_portfolio_app.py) runs Streamlit headless | Both windows, three mandate verdicts and the infeasible-objective stop pass |
| Independent recalculation | All 53,130 grid mixes recalculated from monthly prices without the app or optimizer code. [Model validation](https://github.com/kholliger13/project2-portfolio-app/blob/main/MODEL_VALIDATION.md) | Same winning portfolios and qualifying counts (22,829 and 36,889) |
| Point-in-time gate | [Gate verification](https://github.com/kholliger13/project2-portfolio-app/blob/main/verify_asof.py) against the supplied known answer | All 12 rows and all six signal values match |
| PAYEMS vintages | [PAYEMS verification](https://github.com/kholliger13/project2-portfolio-app/blob/main/payems_verify.py) | Three ALFRED row checks, seven date and boundary cases, shuffled input and duplicate rejection pass |
| Rates and live apps | `verify_rates_app.py`, `verify_asof_app.py` | Cutoffs, two-month PAYEMS trigger, missing values, wrong-vintage and HTML rejection, and caching pass |
| Replay | [Replay script](https://github.com/kholliger13/project2-portfolio-app/blob/main/replay.py) | Both locked vetoes cleared (Section 4) |

## 2. Independent challenge

Using the three parts of Federal Reserve SR 26-2, conceptual soundness, outcome analysis and ongoing monitoring, I would approve the model for classroom demonstration and **hold allocation approval**. The main weakness is window sensitivity. The same mandate puts 55% in LQD with all 59 months and 80% with the last 36. [Full model validation](https://github.com/kholliger13/project2-portfolio-app/blob/main/MODEL_VALIDATION.md)

## 3. Stress run

Base case (all 59 months, 8% objective, at least 20% in LQD + TLT): QQQ 20% / XLE 25% / LQD 55%, estimated 8.31% return at 11.43% volatility.

| Stress | Change | Result | What it means |
|---|---|---|---|
| Estimates | Cut each fund’s return estimate by one percentage point, one fund at a time | Still feasible every time. Cutting LQD changes the mix to QQQ 15% / XLE 30% / LQD 55%. Cutting XLE gives the lowest estimated return, 8.06%. | The base mix has 0.31 percentage points of cushion. Combined estimate errors could put that mix below the hurdle. |
| Window | Last 36 months instead of 59 | XLE 10% / LQD 80% / FBMPX 10%, 8.30% at 7.40% | The window change moves LQD by 25 percentage points. |
| Window (replay) | Fit on first 23 months, hold for last 36 | QQQ 10% / XLE 40% / LQD 50%, realized 11.34% at 9.45% versus equal weight at 15.69% and 9.96% | Both vetoes cleared (Section 4). |
| Costs | 0, 10, 25 and 50 bps on turnover | Constrained net return 11.39% to 11.12%, volatility 9.44% to 9.52% | Both vetoes cleared at all four tested costs. |
| Constraints | Raise objective to 9% or 30%, or raise the bond floor to 40% or 60% | 9% remains feasible (9.09%). At 30% no mix qualifies and the process stops. At a 40% floor the mix is unchanged. At 60% the mix is QQQ 5% / XLE 35% / LQD 60%, estimated at 8.10%. | The 60% floor changes the mix by requiring more LQD than the base allocation's 55%. |

**Conditions that stop the process.** Any one of these stops a recommendation or sends it to the committee:

- No mix meets the objective and the bond floor.
- The replay’s net return falls below 8%, or its volatility is at least equal weight’s.
- The funded sleeve fails a binding mandate rule.
- A required input is missing or was unavailable on the decision date.
- In a live pilot, any fund’s proposed weight moves more than 15 percentage points from the prior month’s proposal.
- Refer the pilot to the committee if the point-in-time PAYEMS change is negative for two consecutive months, each measured in the vintage available the day before that month’s decision.

## 4. Locked Changed-Input Record

**Changed input.** The estimation window. Weights were fitted on the first 23 monthly returns (Nov 2021–Sep 2023) instead of all 59, then held over the last 36 (Oct 2023–Sep 2026). The [locked record](https://github.com/kholliger13/project2-portfolio-app/blob/main/LOCKED_CHANGED_INPUT.md) specifies monthly rebalancing to fixed targets, 10 bps on one-way turnover including the first purchase, geometric annualized net return, and sample standard deviation × √12.

**Vetoes.** Hold the pilot if the constrained mix earns under 8% net or if its volatility is at least equal weight’s.

**Publication history.** The replay prediction was committed locally at [`f6a0689`](https://github.com/kholliger13/project2-portfolio-app/commit/f6a0689) (17:17:53), before the replay commit [`159bf56`](https://github.com/kholliger13/project2-portfolio-app/commit/159bf56) (17:18:59). The repository was first pushed to GitHub later that evening, so GitHub shows the commit order and timestamps, not a pre-run publication. The 50 bp prediction ([`ba706d9`](https://github.com/kholliger13/project2-portfolio-app/commit/ba706d9)) was public on GitHub before its rerun. Both predictions had the AI assistance disclosed above.

| Portfolio | Predicted net return | Actual net return | Predicted volatility | Actual volatility |
|---|---:|---:|---:|---:|
| Constrained | 12% (9–15%) | **11.34%** | 15% (12–18%) | **9.45%** |
| Equal weight | 14% (13–15%) | **15.69%** | 10% (9–11%) | **9.96%** |

| Item | Predicted | Actual |
|---|---|---|
| Qualifying 23-month mix | Yes | Yes (4,964 of 53,130) |
| Weights | 20–25% LQD and 50–65% XLE + EWZ | 50% LQD, 40% XLE and 0% EWZ |
| Veto 1 (return < 8%) | Does not trigger | Did not trigger |
| Veto 2 (volatility ≥ equal weight) | Triggers | **Did not trigger** |
| Vote | Hold | Replay passes. Funding is held pending mandate scope. |

**Why the prediction missed.** It expected the 2022 fit to lean on volatile energy and Brazil funds. The optimizer hit the 8% target with a large LQD position plus XLE. Over the next 36 months, that allocation had lower realized volatility than equal weight. The return call was right and the risk call was wrong.

**Second record: cost, published before its run.** The 50 bp prediction was on GitHub at [`ba706d9`](https://github.com/kholliger13/project2-portfolio-app/commit/ba706d9) before the rerun. It predicted net returns falling by less than 0.5 percentage points, little change in volatility, and the same decision. Actual returns fell by 0.21 points for the constrained mix and 0.24 for equal weight, with volatility up about 0.07 points for each. The funding hold stayed in place. [Partner-swap record](https://github.com/kholliger13/project2-portfolio-app/blob/main/docs/partner-swap.md)

## 5. Cold runs

| Run | Result |
|---|---|
| First attempt, shared course repository | Failed because no Project 2 README was published. Fixed by publishing this repository with its full local history. |
| Zachary’s rerun on `ba706d9`, fresh clone, README only | No failure. About 32 seconds from clone to the final replay line, including setup. |

## 6. One AI output I checked

**The claim.** While helping me tighten the recommendation, Claude wrote that equal weight was a mandate-compliant fallback (10.00% estimated return and 33.3% in LQD + TLT).

**How I checked it.** I recomputed equal weight on the replay’s 23-month fit, because those are the estimates the pilot would be funded on.

**What I found.** The claim held only on the 59-month estimates. On the 23-month fit, equal weight estimates 1.88%, and the 25/75 pilot estimates 3.49%. Both clear the bond floor and fail the 8% screen if it applies to the funded sleeve. A blend needs about 95.24% in the constrained mix to pass.

**What changed.** The recommendation became “hold funding until the scope of the 8% screen is confirmed,” and the memo and Video 3 brief show both readings.

## 7. Limits

- The return figures come from historical estimates and a historical replay. The later 36 months had already been seen.
- Volatility measures variability. Maximum loss requires separate evaluation.
- PAYEMS is admitted for monitoring only. Its captured coverage (Aug 2024–Sep 2026) is too short to test predictive value. It does not set weights.
- The scope of the 8% screen is pending committee confirmation.
