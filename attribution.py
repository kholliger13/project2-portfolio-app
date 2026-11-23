"""Attribute the change in the constrained fit to its three estimated inputs."""

from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

from portfolio_core import (
    OBJECTIVE, RESERVE_ELIGIBLE, RESERVE_MIN, build_covariance, estimate_inputs,
    load_prices, monthly_returns, optimize,
)

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "docs/driver-attribution.md"
INPUTS = ("Return estimates", "Fund volatilities", "Correlations")
METRICS = ("LQD weight", "volatility", "return")
CASES = (
    ("59-month baseline", frozenset()),
    *((f"{name} only", frozenset({name})) for name in INPUTS),
    ("24-month answer", frozenset(INPUTS)),
)


def analyze(returns):
    """Fit each combination once and average its marginal effects over all orders."""
    if len(returns) != 59:
        raise ValueError("The window attribution requires 59 monthly returns.")

    baseline = estimate_inputs(returns)
    recent = estimate_inputs(returns.tail(24))
    fits = {}
    for size in range(len(INPUTS) + 1):
        for subset in combinations(INPUTS, size):
            swaps = frozenset(subset)
            mean, vol, corr = (
                recent[i] if name in swaps else baseline[i]
                for i, name in enumerate(INPUTS)
            )
            fit = optimize(mean, build_covariance(vol, corr), RESERVE_ELIGIBLE,
                           OBJECTIVE, RESERVE_MIN)
            if not fit["found"]:
                raise ValueError(f"No qualifying mix for swaps: {subset!r}")
            fits[swaps] = fit

    # Exact rational arithmetic makes the marginal changes telescope without
    # floating-point rounding after the optimizer has returned its estimates.
    outcomes = {
        swaps: dict(zip(METRICS, map(Fraction, (
            float(fit["weights"]["LQD"]), fit["volatility"], fit["return"],
        ))))
        for swaps, fit in fits.items()
    }
    effects = {name: dict.fromkeys(METRICS, Fraction(0)) for name in INPUTS}
    orders = tuple(permutations(INPUTS))
    for order in orders:
        swaps = frozenset()
        for name in order:
            updated = swaps | {name}
            for metric in METRICS:
                effects[name][metric] += (
                    outcomes[updated][metric] - outcomes[swaps][metric]
                ) / len(orders)
            swaps = updated

    total = {
        metric: outcomes[frozenset(INPUTS)][metric] - outcomes[frozenset()][metric]
        for metric in METRICS
    }
    for metric in METRICS:
        assert sum(effects[name][metric] for name in INPUTS) == total[metric], metric
    return fits, {**effects, "Total": total}


def render(fits, effects):
    lines = [
        "# Driver attribution",
        "",
        "What drove the change from the 59-month to the 24-month answer?",
        "",
        "## One-at-a-time swaps",
        "",
        "Each swap replaces one input with its shorter-window estimate and refits "
        "the portfolio under the original constraints. The final row swaps every input.",
        "",
        "| Case | Weights | Estimated return | Estimated volatility | LQD |",
        "|---|---|---:|---:|---:|",
    ]
    for label, swaps in CASES:
        fit = fits[swaps]
        weights = ", ".join(
            f"{ticker} {weight:.0%}" for ticker, weight in fit["weights"].items() if weight
        )
        lines.append(f"| {label} | {weights} | {fit['return']:.2%} | "
                     f"{fit['volatility']:.2%} | {fit['weights']['LQD']:.0%} |")

    lines.extend([
        "",
        "## Shapley attribution",
        "",
        "The table averages the change contributed by each input across every swap "
        "order. All contributions are in percentage points.",
        "",
        "| Input | LQD weight change | Volatility change | Estimated return change |",
        "|---|---:|---:|---:|",
    ])
    for name, row in effects.items():
        cells = " | ".join(f"{float(row[metric] * 100):+.2f}" for metric in METRICS)
        lines.append(f"| {name} | {cells} |")

    lines.extend([
        "",
        "Updated return estimates raised the fitted LQD weight the most. They let "
        "the optimizer clear the return hurdle with less equity exposure. Updated "
        "correlations partly offset that shift and contributed most of the gain in "
        "estimated return. Lower fund volatilities explained the largest share of "
        "the drop in portfolio volatility, with correlations contributing the next "
        "largest share. The volatility swap alone lowered portfolio volatility "
        "while keeping the baseline weights.",
        "",
        "Codex built this script; the interpretation and decision are mine.",
    ])
    return "\n".join(lines) + "\n"


def main():
    returns = monthly_returns(load_prices(ROOT / "prices.csv"))
    report = render(*analyze(returns))
    print(report, end="")
    if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report:
        REPORT.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
