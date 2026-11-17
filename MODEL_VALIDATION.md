# Independent challenge of the portfolio model

**Would I approve a portfolio allocation based on this model?** I would approve it for classroom demonstrations and hold allocation approval. The grid search is reproducible. A reviewer can still reject its use for an allocation if the assumptions fail the mandate, the results deteriorate on unseen data, or the inputs fail an availability check. This applies the three validation components in [Federal Reserve SR 26-2, Section V](https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm).

## Conceptual Soundness

The Lab 14 app minimizes estimated volatility across long-only, fully invested portfolios in 5-percentage-point steps. It uses annualized historical arithmetic returns, historical covariance, an 8% return objective, and a 20% floor in LQD and TLT. The result is conditional on those estimates, the grid, and the reserve definition.

I recalculated all 53,130 mixes directly from the bundled monthly prices, using each mix's weighted monthly return series to calculate its mean and sample standard deviation. This calculation used no portfolio app or optimizer code. Both winning portfolios and the qualifying counts matched the app (22,829 and 36,889). Call this an independent calculation method. An independent reviewer still needs to judge whether the method fits the decision.

| Estimation window | LQD | Estimated annual return | Estimated annual volatility |
|---|---:|---:|---:|
| All 59 months | 55% | 8.31% | 11.43% |
| Last 36 months | 80% | 8.30% | 7.40% |

**Grounds to reject.** Require a documented rationale for the estimation window and reserve designation before relying on the weights. The window change alone raises LQD by 25 percentage points. For a Meridian allocation, independently verify reserve eligibility, liquidity, payout coverage and the other investment policy limits. Meridian's CPI + 4% objective after costs over rolling five-year periods requires evidence beyond the app's nominal historical return estimate. Estimated volatility also cannot establish compliance with the unresolved calendar-year loss provision. [Lab 14 evidence](evidence/Lab14_portfolio_app_2026_10_22.md) · [Meridian policy case](evidence/meridian_foundation_common_case.md)

## Outcome Analysis

The two windows overlap, and each portfolio is evaluated on the same returns used to choose it. The 7.40% volatility therefore describes the estimation sample. Realized performance remains untested in this review.

**Grounds to reject.** Before looking at results, agree on the benchmark, test period, rebalance schedule, costs and acceptable deviations. At each historical rebalance, estimate using only data available then, freeze the weights, and evaluate the next period's realized return, volatility, drawdown, turnover and reserve coverage. Compare against a simple feasible baseline on the same dates and cost assumptions. A binding mandate breach or a persistent shortfall outside agreed tolerances supports holding or rejecting the proposed use. The bundled 59 monthly returns cannot supply even one complete five-year outcome after a 36-month estimation period. That evidence gap matters for Meridian's five-year objective. [Frozen price inputs](prices.csv)

If PAYEMS enters a future backtest, require the correct vintage at each decision before measuring performance. On October 4, 2024, September employment appears only when same-day releases are eligible. Reject a backtest that uses that value before the release even if its reported performance improves. The current PAYEMS test establishes a date boundary within the captured data. [Source-to-test trace](DECISION.md)

## Ongoing Model Monitoring

**Proposed for any future approved use.** At each scheduled rebalance and after a material data or model change, have the model owner record the input snapshot, proposed weights, constraint results and changes since the previous run. An independent reviewer should check vintage integrity, reserve eligibility and coverage, concentration, turnover and realized performance against pre-agreed tolerances. Use the observed 25-point LQD swing as evidence for reviewing threshold choices before use.

**Grounds to suspend use.** Block a recommendation when a required input is missing or too recent for the decision, or when a binding mandate rule fails. Escalate persistent model-versus-realized deviations or large allocation changes beyond an agreed tolerance. Record the cause and retest before restoring decision use.

This review adds evidence for the existing committee decision and leaves the [frozen must-fix list](MUST_FIX.md) in force.
