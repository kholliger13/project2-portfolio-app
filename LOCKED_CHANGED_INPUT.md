# Project 2 | Changed-Input Record

**Status:** Pre-run protocol saved. The lock is pending Kayla's AI-off prediction and GitHub commit. Replay results are pending.

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

## AI-off prediction | Kayla completes before running

| Portfolio | Predicted annualized net return | Predicted annualized volatility |
|---|---|---|
| Constrained | | |
| Equal weight | | |

- Qualifying fit expected
- 8% return veto expected to trigger
- Relative-volatility veto expected to trigger
- Predicted decision and reason
- Pre-run GitHub commit link

## Replay record | Complete after the prediction is committed

Record the run command, training and evaluation dates, qualifying mix count, weights, both portfolios' outcome measures, the net-return gap, pilot mandate checks, and the committee decision. Compare the results with the prediction.
