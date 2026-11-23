# Validation and AI use

**AI use.** I used OpenAI Codex to implement, test and document the app, the replay and this repository. I used Claude (Anthropic) to review my plan, draft the 23/36 replay prediction and the 50 bp cost prediction at my request, and run one independent cold run of the README. **I wrote the Locked Changed-Input Record prediction (24-month window) myself, without AI.** Claude suggested the input to test and the template. The prediction values and reasoning are mine. The analysis and the decision are mine. This is education, not investment advice.

[Project 2 repository](https://github.com/kholliger13/project2-portfolio-app)

## Sources and as-of boundary

- **Fund prices.** Yahoo Finance monthly adjusted closes in `prices.csv`, downloaded October 22, 2026. The file yields 59 monthly returns from November 2021 through September 2026. [Price source and download record](https://github.com/kholliger13/project2-portfolio-app/blob/main/evidence/Lab14_portfolio_app_2026_10_22.md)

- **PAYEMS.** Captured ALFRED vintages cover August 2024 through September 2026. The latest captured vintage is October 2, 2026. Under the previous-day eligibility rule, only vintages dated before the decision date are eligible. [PAYEMS vintage record](https://github.com/kholliger13/project2-portfolio-app/blob/main/evidence/Lab15_PAYEMS_point_in_time_2026_10_27.md) · [Previous-day rule](https://github.com/kholliger13/project2-portfolio-app/blob/main/docs/decision-memo.md)

- **Decision as-of date for fund prices.** September 2026, the last price month used.

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
| Replay | [Replay script](https://github.com/kholliger13/project2-portfolio-app/blob/main/replay.py) | Both locked vetoes cleared (Section 5) |
| Numbers audit | [verify_claims.py](https://github.com/kholliger13/project2-portfolio-app/blob/main/verify_claims.py) recomputes every headline figure cited in the README, memo, results and validation documents and fails the review if any differs. A self-test confirms it catches a changed number. | 261 claims pass. The self-test catches the altered figure. |

## 2. Independent challenge

Using the three parts of Federal Reserve SR 26-2, conceptual soundness, outcome analysis and ongoing monitoring, the independent review supported classroom demonstration and recommended holding allocation approval pending mandate clarification. The November 19 decision memo records how that clarification led to a limited pilot with review triggers. The main weakness is window sensitivity. The same mandate puts 55% in LQD with all 59 months and 80% with the last 36. [Full model validation](https://github.com/kholliger13/project2-portfolio-app/blob/main/MODEL_VALIDATION.md)

## 3. Stress run

Base case (all 59 months, 8% objective, at least 20% in LQD + TLT): QQQ 20% / XLE 25% / LQD 55%, estimated 8.31% return at 11.43% volatility.

| Stress | Change | Result | What it means |
|---|---|---|---|
| Estimates | Cut each fund’s return estimate by one percentage point, one fund at a time | Still feasible every time. Cutting LQD changes the mix to QQQ 15% / XLE 30% / LQD 55%. Cutting XLE gives the lowest estimated return, 8.06%. | The base mix has 0.31 percentage points of cushion. Combined estimate errors could put that mix below the hurdle. |
| Window | Last 36 months instead of 59 | XLE 10% / LQD 80% / FBMPX 10%, 8.30% at 7.40% | The window change moves LQD by 25 percentage points. |
| Window (replay) | Fit on first 23 months, hold for last 36 | QQQ 10% / XLE 40% / LQD 50%, realized 11.34% at 9.45% versus equal weight at 15.69% and 9.96% | Both vetoes cleared (Section 5). |
| Costs | 0, 10, 25 and 50 bps on turnover | Constrained net return 11.39% to 11.12%, volatility 9.44% to 9.52% | Both vetoes cleared at all four tested costs. |
| Constraints | Raise objective to 9% or 30%, or raise the bond floor to 40% or 60% | 9% remains feasible (9.09%). At 30% no mix qualifies and the process stops. At a 40% floor the mix is unchanged. At 60% the mix is QQQ 5% / XLE 35% / LQD 60%, estimated at 8.10%. | The 60% floor changes the mix by requiring more LQD than the base allocation's 55%. |

**Conditions that stop the process.** Any one of these stops a recommendation or sends it to the committee:

- No mix meets the objective and the bond floor.
- The replay’s net return falls below 8%, or its volatility is at least equal weight’s.
- The funded sleeve fails a binding mandate rule.
- A required input is missing or was unavailable on the decision date.
- In a live pilot, any fund’s proposed weight moves more than 15 percentage points from the prior month’s proposal.
- Refer the pilot to the committee if the point-in-time PAYEMS change is negative for two consecutive months, each measured in the vintage available the day before that month’s decision.

## 4. Locked Changed-Input Record (requirement 6)

**Record.** [24-month prediction](https://github.com/kholliger13/project2-portfolio-app/blob/main/docs/locked-record-24-month.md).

**Provenance.** I wrote this prediction myself, without AI. Claude suggested the input to test and the template; the prediction values and reasoning are mine.

**Immutable pre-run commit.** Verified [`ee774a4`](https://github.com/kholliger13/project2-portfolio-app/commit/ee774a48385672d4ef86fcbcda76412fac70f0fe) on GitHub before the test. The commit is dated Nov 19, 2026, 4:12:42 PM ET. The run began at 4:14:18 p.m. ET.

**Input changed.** Estimation window, **old value** all 59 monthly returns, **new value** the last 24 monthly returns (Oct 2024–Sep 2026). Held fixed: 8% objective, at least 20% LQD + TLT, 5-point grid, long-only, minimum volatility.

| Field | My prediction | Actual |
|---|---|---|
| Qualifying mix found? | Yes | Yes (31,774 of 53,130) |
| Weights | 45% LQD, 0% TLT, 55% equities | 60% LQD, 0% TLT, 40% equities (QQQ 20, XLE 15, EWZ 5) |
| Estimated return | 8.4% | 8.79% |
| Volatility | 12.0% | 6.70% |
| Direction vs. 59-month answer (8.31% / 11.43%, LQD 55%) | Slightly higher return and volatility, LQD down 10 points | Return up (as predicted); volatility down 4.73 points; LQD up 5 points |
| Effect on the decision | Keep the 8% objective and shift 10 points from LQD to equities | No change to the decision. At the time of the run, funding was on hold pending the 8% scope; that was resolved Nov 19 and the recommendation is now a 25% pilot (see the decision memo). |

**My reasoning before the run.** The shorter window will estimate a lower return for LQD relative to equities, so the minimum-volatility mix that clears 8% will need more equity exposure. That shift should raise volatility slightly. LQD should fill the bond allocation because TLT's longer duration makes it more sensitive to rate moves.

**What happened and why.** **Failure diagnosis.** The return direction and TLT at 0% were right; the weights and volatility went the opposite way. My premise held: over the last 24 months the equity estimates rose (QQQ 16.0% to 23.1%, FBMPX 14.7% to 25.3%) while LQD's estimate barely moved (-0.9% to -0.4%). But because the 8% target is fixed, higher equity returns let the optimizer reach 8% with fewer equities, so it held more LQD, not less. LQD's volatility also fell from 9.9% to 5.6% in the shorter window, which lowered total volatility instead of raising it. Correlations partly offset the shift, cutting LQD by 5 points, so the net change was +5 points rather than +10 ([driver attribution](https://github.com/kholliger13/project2-portfolio-app/blob/main/docs/driver-attribution.md)). The decision does not change. Across three windows LQD is 55%, 80% and 60% under the same mandate, which supports the window-instability finding and the 15-point monitoring trigger. Claude helped me interpret the result; the prediction above was written without AI. [Driver attribution](https://github.com/kholliger13/project2-portfolio-app/blob/main/docs/driver-attribution.md)

## 5. Supporting evidence: 23/36 historical replay

The 23/36 replay and the 50 bp cost check are supporting evidence. Section 4 contains the prediction for requirement 6.

**Provenance.** Claude drafted the 23/36 prediction at my request before the replay, and I adopted it. The prediction was committed locally at [`f6a0689`](https://github.com/kholliger13/project2-portfolio-app/commit/f6a0689) (Nov 17, 17:17:53 ET), before the replay commit [`159bf56`](https://github.com/kholliger13/project2-portfolio-app/commit/159bf56) (17:18:59 ET). The repository was first pushed to GitHub later that evening.

**Design.** Weights were fitted on the first 23 monthly returns (Nov 2021–Sep 2023) and held over the last 36 (Oct 2023–Sep 2026). Both portfolios were rebalanced monthly to fixed targets, with 10 bps on one-way turnover, including the first purchase. [Full replay rules](https://github.com/kholliger13/project2-portfolio-app/blob/main/LOCKED_CHANGED_INPUT.md)

**Vetoes.** Hold the pilot if the constrained mix earns under 8% net or if its volatility is at least equal weight’s.

| Portfolio | Predicted net return | Actual net return | Predicted volatility | Actual volatility |
|---|---:|---:|---:|---:|
| Constrained | 12% (9–15%) | **11.34%** | 15% (12–18%) | **9.45%** |
| Equal weight | 14% (13–15%) | **15.69%** | 10% (9–11%) | **9.96%** |

Both vetoes cleared. The prediction expected the volatility veto to trigger. The fitted mix held 50% LQD and 40% XLE and had lower realized volatility than equal weight over the following 36 months.

**Cost check.** Claude drafted the separate 50 bp prediction at my request. It was public on GitHub at [`ba706d9`](https://github.com/kholliger13/project2-portfolio-app/commit/ba706d9) before its rerun. Net returns fell 0.21 percentage points for the constrained mix and 0.24 for equal weight. Volatility rose about 0.07 points for each. Both vetoes cleared, as predicted. [Partner-swap record](https://github.com/kholliger13/project2-portfolio-app/blob/main/docs/partner-swap.md)

## 6. Cold runs

| Run | Result |
|---|---|
| First attempt, shared course repository | Failed because no Project 2 README was published. Fixed by publishing this repository with its full local history. |
| Zachary Alvin, `add3cce`, Nov 19 | The completed fresh clone passed in about 46 seconds including setup. The first clone was retried after network access returned. No repository fix was needed. |
| Claude (Anthropic), `ba706d9`, Nov 17 | No failure. About 32 seconds including setup. |

## 7. One AI output I checked

**The claim.** While helping me tighten the recommendation, Claude wrote that equal weight was a mandate-compliant fallback (10.00% estimated return and 33.3% in LQD + TLT).

**How I checked it.** I recomputed equal weight on the replay’s 23-month fit, to test the fallback under the historical estimates used in the replay.

**What I found.** The claim held only on the 59-month estimates. On the 23-month fit, equal weight estimates 1.88%, and the 25/75 pilot estimates 3.49%. Both clear the bond floor and fail the 8% screen if it applies to the funded sleeve. A blend needs about 95.24% in the constrained mix to pass.

**What changed.** The historical check exposed the funding risk of applying the 23-month estimates to the whole sleeve. Following the professor’s guidance, I apply the screen to decision-date estimates. The funded 25/75 blend clears 8% in all three windows, supporting the pilot. [Decision memo](https://github.com/kholliger13/project2-portfolio-app/blob/main/docs/decision-memo.md#portfolio-pilot-decision)

## 8. Limits

- The return figures come from historical estimates and a historical replay. The later 36 months had already been seen.
- Volatility measures variability. Maximum loss requires separate evaluation.
- PAYEMS is admitted for monitoring only. Its captured coverage (Aug 2024–Sep 2026) is too short to test predictive value. It does not set weights.
- The funding screen uses estimates available at the decision date. Expansion beyond 25% requires six months of live results that clear both replay vetoes.
