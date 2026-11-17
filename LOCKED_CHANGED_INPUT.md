# Project 2 | Changed-Input Record

**Status:** The prediction below supersedes the earlier version and is the one to use for the replay. The local pre-run commit is saved. The GitHub lock and replay remain pending.

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

Pre-run GitHub commit link: pending.

## Replay record | Complete after the prediction is committed

Record the run command, training and evaluation dates, qualifying mix count, weights, both portfolios' outcome measures, the net-return gap, pilot mandate checks, and the committee decision. Compare the results with the prediction.
