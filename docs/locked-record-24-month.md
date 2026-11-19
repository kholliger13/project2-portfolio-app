# Locked Changed-Input Record — 24-month window (AI-off)

Written by me without AI assistance. Claude suggested the input and template. The prediction values and reasoning are mine.

**Pre-run GitHub publication:** verified [`ee774a4`](https://github.com/kholliger13/project2-portfolio-app/commit/ee774a48385672d4ef86fcbcda76412fac70f0fe) on GitHub `main` before running the test. The commit is dated November 19, 2026 at 4:12:42 p.m. ET. The run started at 4:14:18 p.m. ET.

**Input changed:** estimation window

**Old value:** all 59 monthly returns

**New value:** last 24 monthly returns (Oct 2024–Sep 2026)

**Held fixed:** 8% objective, ≥20% LQD + TLT, 5-point grid, long-only, minimum volatility

| Field | Prediction for Oct 2024–Sep 2026 |
|---|---|
| Qualifying mix found? | Yes |
| Predicted weights | 45% LQD, 0% TLT, 55% equities |
| Predicted estimated return | 8.4% |
| Predicted volatility | 12.0% |
| Direction vs. the 59-month answer | Slightly higher return and volatility, with LQD down 10 percentage points |
| Expected effect on the decision | Keep the 8% objective and shift 10 percentage points from LQD to equities. |

**Reasoning.** My guess is that the shorter window will estimate a lower return for LQD relative to equities, so the minimum-volatility mix that clears 8% will need more equity exposure. I expect that shift to raise volatility slightly, and I'm guessing LQD will fill the bond allocation because TLT's longer duration makes it more sensitive to rate moves. These are pre-run guesses, with equities shown as a combined allocation.

## Result

| Field | All 59 returns | Last 24 returns |
|---|---:|---:|
| Qualifying mixes | 22,829 / 53,130 | 31,774 / 53,130 |
| QQQ | 20% | 20% |
| XLE | 25% | 15% |
| EWZ | 0% | 5% |
| LQD | 55% | 60% |
| TLT | 0% | 0% |
| FBMPX | 0% | 0% |
| Estimated annual return | 8.3063% | 8.7948% |
| Annualized volatility | 11.4256% | 6.6991% |
| LQD + TLT | 55% | 60% |

**Prediction comparison.** A mix qualified, TLT stayed at zero and estimated return rose by 0.49 percentage points, matching those directions. LQD rose by 5 percentage points instead of falling by 10, and estimated volatility fell by 4.73 points. In the shorter window, LQD’s estimated volatility fell from 9.87% to 5.64%, and the equity sleeves still supplied enough estimated return for a mix with 60% LQD to clear 8%.

**Decision.** Keep the 8% objective and hold funding pending mandate scope. The 24-month fit supports no shift from LQD to equities. Its return and volatility are in-sample estimates, and the funded-blend check remains separate.

### Reproduce

From the repository root after README setup:

```sh
python - <<'PYTHON'
from portfolio_core import (
    OBJECTIVE, RESERVE_ELIGIBLE, RESERVE_MIN, build_covariance, estimate_inputs,
    load_prices, monthly_returns, optimize,
)

returns = monthly_returns(load_prices("prices.csv"))
assert len(returns) == 59
for label, window in (("All returns", returns), ("Last 24 returns", returns.tail(24))):
    mean, volatility, correlation = estimate_inputs(window)
    result = optimize(mean, build_covariance(volatility, correlation),
                      RESERVE_ELIGIBLE, OBJECTIVE, RESERVE_MIN)
    print(f"{label}: {window.index[0]:%Y-%m} to {window.index[-1]:%Y-%m}; {len(window)} returns")
    print(f"Qualifying mixes: {result['mixes_qualifying']:,} / {result['mixes_tested']:,}")
    if result["found"]:
        print(", ".join(f"{fund} {weight:.2%}" for fund, weight in result["weights"].items()))
        print(f"Estimated return: {result['return']:.4%}; volatility: {result['volatility']:.4%}; "
              f"LQD + TLT: {result['reserves']:.2%}")
PYTHON
```
