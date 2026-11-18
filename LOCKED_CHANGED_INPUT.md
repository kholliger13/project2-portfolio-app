# Project 2 | Changed-Input Record

**Status:** The prediction below supersedes the earlier version and is the one to use for the replay. The prediction was saved locally at `f6a0689` before the run. The replay has been completed under that local lock. GitHub publication followed the replay. The public commit history preserves the local lock and replay order.

## Decision and changed input

Start a 25% constrained pilot only if the replay passes and the 25/75 blend clears the applicable mandate checks. Rebalance to fixed target weights monthly. If the replay fails, hold the pilot and use equal weight as the fallback, subject to the applicable mandate. Equal weight holds 33.3% in LQD and TLT and clears the 20% bond floor. Consider increasing toward 50% only after a genuinely unseen test passes as well.

Use the first 23 monthly returns to fit weights in place of the 59-return fit. Evaluate those weights on the following 36 months. Prior analysis has already used that later window, so this is a historical replay.

## Pre-specified replay rules

- Fit using the app's minimum-volatility search on a long-only, fully invested 5-point grid. Require annualized estimated return of at least 8% and combined LQD and TLT exposure of at least 20%. A fit with zero qualifying portfolios fails the replay.
- Apply the fitted allocation and equal weight to the same 36 months. Rebalance both to fixed weights monthly. Charge 10 basis points times one-way turnover. Count the first purchase as 100% turnover for each portfolio. For subsequent rebalances, one-way turnover is half the sum of absolute differences between drifted and target weights.
- Report geometric annualized net return by compounding all 36 net monthly returns, raising the result to the power of 12/36, and subtracting one. Report annualized volatility as the sample standard deviation of the monthly net returns times the square root of 12.
- Hold the pilot if the constrained mix earns less than 8% annualized after costs or has realized volatility at least as high as equal weight. Report the net-return gap without using it as a third veto.
- Show the proposed pilot weights using 25% of the replay-fit allocation and 75% equal weight. Report the checks supported by those weights, including the LQD and TLT share, and identify any applicable mandate decisions still open.
- In a live pilot, compare each month's newly proposed optimizer weights with the prior proposal. Refer any absolute change greater than 15 percentage points in a fund to the committee.

## Locked Changed-Input Record — prediction

Committed locally: 2026-11-17T17:17:53-05:00 before running the 23/36 replay.

Replay: weights fitted on first 23 monthly returns (Nov 2021–Sep 2023); held over
last 36 (Oct 2023–Sep 2026), monthly rebalance to fixed targets, 10 bps on turnover
including the initial trade. Geometric annualized net return; sample stdev × √12.

| Portfolio | Predicted net return (ann.) | Predicted volatility (ann.) |
|---|---:|---:|
| Constrained mix | 12% (range 9–15%) | 15% (range 12–18%) |
| Equal weight | 14% (range 13–15%) | 10% (range 9–11%) |

- Qualifying 23-month mix found? Yes
- Predicted weights: about 20–25% LQD (the floor, little or no TLT), heavy XLE and EWZ (together 50–65%), small QQQ/FBMPX.
- Veto 1 (constrained net return < 8%): does not trigger
- Veto 2 (constrained vol >= equal-weight vol): triggers
- Resulting vote: hold at 100% equal weight

Reasoning: The first 23 months include the 2022 rate shock, so LQD, TLT, QQQ and
FBMPX all show weak or negative averages, while energy (XLE) and Brazil (EWZ) look
strong. To clear 8% with a 20% bond floor, the optimizer must lean on XLE and EWZ —
volatile, concentrated funds — and it underweights QQQ and FBMPX, the strongest
funds afterward. The mix should still clear 8%, but equal weight's broad spread
had only ~10% volatility over the last 36 months, so I expect the constrained
mix to be riskier, which fails the claim.

Local pre-run commit, later published on GitHub: [`f6a0689`](https://github.com/kholliger13/project2-portfolio-app/commit/f6a06897cd0d42c4574cf65961833846c0738159).

## Replay result | November 17, 2026

Run `python replay.py` from the repository root after installing the pinned dependencies. The fit used November 2021–September 2023 and the evaluation used October 2023–September 2026. Rebalances occur before each month's return. Execution costs reduce beginning-of-month value, with no terminal liquidation. A separate calculation verified net return, volatility and the blend's training-period return.

**The replay passed both vetoes. Pilot funding remains conditional on mandate clearance.** The optimizer found 4,964 qualifying mixes out of 53,130. The winner's estimated training return was 8.3060% and its estimated training volatility was 17.2810%.

| Portfolio | Annualized net return | Annualized volatility |
|---|---:|---:|
| Constrained mix | 11.3370% | 9.4545% |
| Equal weight | 15.6934% | 9.9588% |

The constrained mix cleared the 8% hurdle and was 0.5043 percentage points less volatile. Its net return trailed equal weight by 4.3565 percentage points using unrounded results. The pre-specified rules report that gap without treating it as a veto.

| Fund | Constrained fit | Equal weight | Proposed 25/75 pilot |
|---|---:|---:|---:|
| QQQ | 10.0% | 16⅔% | 15.0% |
| XLE | 40.0% | 16⅔% | 22.5% |
| EWZ | 0.0% | 16⅔% | 12.5% |
| LQD | 50.0% | 16⅔% | 25.0% |
| TLT | 0.0% | 16⅔% | 12.5% |
| FBMPX | 0.0% | 16⅔% | 12.5% |

**Pilot mandate check.** The blend is long-only and sums to 100%. Its 37.50% bond weight clears the 20% floor. Its training-period estimated return is 3.4864%, below 8%. If the 8% estimated-return screen applies to the funded sleeve as a whole, both the blend and the equal-weight fallback (1.88% on the same fit) fail. A 50/50 blend estimates 5.09%. Meeting 8% would take about 95% constrained, outside the pilot range. Funding stays on hold. Confirm that scope before funding. The later-period return hurdle was tested on the constrained mix under the locked rules. Expansion still requires a genuinely unseen test.

**Prediction comparison.** A qualifying fit and a return above 8% were correctly predicted. The constrained net return was within the predicted range. Its volatility was below the predicted range and below equal weight's, reversing the predicted volatility veto. Equal weight's volatility was within the predicted range and its net return exceeded the predicted range. The fitted portfolio held 50% LQD and zero EWZ, differing from the predicted 20–25% LQD and 50–65% combined XLE and EWZ.
