"""Run the locked Project 2 historical replay on the bundled six-fund prices."""

from math import prod, sqrt
from pathlib import Path
from statistics import stdev

import pandas as pd

from portfolio_core import (
    OBJECTIVE,
    RESERVE_ELIGIBLE,
    RESERVE_MIN,
    build_covariance,
    estimate_inputs,
    load_prices,
    monthly_returns,
    optimize,
)

TRADE_COST = 0.001


def evaluate(returns, target):
    """Rebalance before each month's return and charge costs on one-way turnover."""
    drifted = target
    net_returns = []
    for month, (_, changes) in enumerate(returns.iterrows()):
        turnover = 1.0 if month == 0 else (target - drifted).abs().sum() / 2
        gross_end = target * (1 + changes)
        gross_growth = gross_end.sum()
        net_returns.append((1 - TRADE_COST * turnover) * gross_growth - 1)
        drifted = gross_end / gross_growth
    return (
        prod(1 + value for value in net_returns) ** (12 / len(net_returns)) - 1,
        stdev(net_returns) * sqrt(12),
    )


def main():
    prices = load_prices(Path(__file__).with_name("prices.csv"))
    returns = monthly_returns(prices)
    if len(returns) != 59:
        raise ValueError("The locked replay requires 59 monthly returns.")
    training, evaluation = returns.iloc[:23], returns.iloc[23:]
    estimated_returns, volatility, correlations = estimate_inputs(training)
    fit = optimize(
        estimated_returns, build_covariance(volatility, correlations),
        RESERVE_ELIGIBLE, OBJECTIVE, RESERVE_MIN,
    )
    equal = pd.Series(1 / len(returns.columns), index=returns.columns)
    equal_return, equal_volatility = evaluate(evaluation, equal)
    print(f"Fit: {training.index[0]:%Y-%m} to {training.index[-1]:%Y-%m}")
    print(f"Replay: {evaluation.index[0]:%Y-%m} to {evaluation.index[-1]:%Y-%m}")
    print(f"Qualifying mixes: {fit['mixes_qualifying']:,} / {fit['mixes_tested']:,}")
    print(f"Equal weight: net return {equal_return:.4%}, volatility {equal_volatility:.4%}")
    if not fit["found"]:
        print("HOLD: no qualifying training mix. No fitted blend to check.")
        return

    target = fit["weights"]
    net_return, realized_volatility = evaluate(evaluation, target)
    return_veto = net_return < OBJECTIVE
    risk_veto = realized_volatility >= equal_volatility
    print(f"Constrained fit: estimated return {fit['return']:.4%}, "
          f"estimated volatility {fit['volatility']:.4%}")
    print(f"Constrained replay: net return {net_return:.4%}, volatility {realized_volatility:.4%}")
    print(f"Net return gap vs equal weight: {(net_return - equal_return) * 100:+.4f} pp")
    print(f"Return veto: {return_veto}; volatility veto: {risk_veto}")

    blend = 0.25 * target + 0.75 * equal
    weights = pd.DataFrame({"Constrained": target, "Equal": equal, "25/75 blend": blend})
    print(weights.to_string(float_format=lambda weight: f"{weight:.4%}"))
    blend_reserve = blend.loc[sorted(RESERVE_ELIGIBLE)].sum()
    blend_return = blend @ estimated_returns
    print(f"Blend: total weight {blend.sum():.4%}, long-only {bool((blend >= 0).all())}, "
          f"bond weight {blend_reserve:.4%}, training return estimate {blend_return:.4%}")
    if return_veto or risk_veto:
        print("HOLD: replay failed. Keep equal weight as the fallback subject to policy.")
    else:
        print("PASS: replay clears both vetoes. Check the blend against the full mandate.")


if __name__ == "__main__":
    main()
