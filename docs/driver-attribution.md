# Driver attribution

What drove the change from the 59-month to the 24-month answer?

## One-at-a-time swaps

Each swap replaces one input with its shorter-window estimate and refits the portfolio under the original constraints. The final row swaps every input.

| Case | Weights | Estimated return | Estimated volatility | LQD |
|---|---|---:|---:|---:|
| 59-month baseline | QQQ 20%, XLE 25%, LQD 55% | 8.31% | 11.43% | 55% |
| Return estimates only | XLE 20%, LQD 65%, FBMPX 15% | 8.08% | 10.82% | 65% |
| Fund volatilities only | QQQ 20%, XLE 25%, LQD 55% | 8.31% | 8.83% | 55% |
| Correlations only | QQQ 25%, XLE 15%, EWZ 10%, LQD 50% | 8.53% | 9.46% | 50% |
| 24-month answer | QQQ 20%, XLE 15%, EWZ 5%, LQD 60% | 8.79% | 6.70% | 60% |

## Shapley attribution

The table averages the change contributed by each input across every swap order. All contributions are in percentage points.

| Input | LQD weight change | Volatility change | Estimated return change |
|---|---:|---:|---:|
| Return estimates | +10.00 | -0.56 | +0.00 |
| Fund volatilities | +0.00 | -2.55 | +0.05 |
| Correlations | -5.00 | -1.62 | +0.44 |
| Total | +5.00 | -4.73 | +0.49 |

Updated return estimates raised the fitted LQD weight the most. They let the optimizer clear the return hurdle with less equity exposure. Updated correlations partly offset that shift and contributed most of the gain in estimated return. Lower fund volatilities explained the largest share of the drop in portfolio volatility, with correlations contributing the next largest share. The volatility swap alone lowered portfolio volatility while keeping the baseline weights.

Codex built this script; the interpretation and decision are mine.
