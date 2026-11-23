"""Check portfolio figures against the bundled data and their Markdown citations."""

import argparse
import re
from pathlib import Path
from tempfile import TemporaryDirectory

from attribution import CASES, analyze
from portfolio import equal_weights, portfolio_volatility
from portfolio_core import (
    OBJECTIVE, RESERVE_ELIGIBLE, RESERVE_MIN, build_covariance, choose_window,
    estimate_inputs, load_prices, monthly_returns, optimize,
)
from replay import evaluate, minimum_constrained_share

ROOT = Path(__file__).resolve().parent
DOCUMENTS = {
    "readme": "README.md",
    "memo": "docs/decision-memo.md",
    "validation": "docs/validation-and-ai-use.md",
    "results": "docs/results.md",
    "24-month record": "docs/locked-record-24-month.md",
    "replay record": "LOCKED_CHANGED_INPUT.md",
    "partner swap": "docs/partner-swap.md",
    "driver attribution": "docs/driver-attribution.md",
}


def select_fit(mean, covariance, objective=OBJECTIVE, floor=RESERVE_MIN):
    return optimize(mean, covariance, RESERVE_ELIGIBLE, objective, floor)


def model_values():
    returns = monthly_returns(load_prices(ROOT / "prices.csv"))
    if len(returns) != 59:
        raise ValueError("Expected 59 monthly returns for the locked comparisons.")
    equal = returns.iloc[0].copy()
    equal[:] = equal_weights(returns.columns)
    values = {}
    windows = {59: returns, 36: choose_window(returns, 36),
               24: returns.tail(24), 23: returns.head(23)}
    for months, window in windows.items():
        mean, vol, corr = estimate_inputs(window)
        covariance = build_covariance(vol, corr)
        fit = select_fit(mean, covariance)
        target = fit["weights"]
        prefix = str(months)
        for field in ("return", "volatility", "reserves", "mixes_qualifying", "mixes_tested"):
            values[f"{prefix} {field}"] = fit[field]
        for ticker in target.index:
            values[f"{prefix} {ticker} weight"] = target[ticker]
            values[f"{prefix} {ticker} estimate"] = mean[ticker]
            values[f"{prefix} {ticker} volatility"] = vol[ticker]
        for name, weights in (
            ("equal", equal), ("blend", 0.25 * target + 0.75 * equal),
            ("halfway", 0.5 * target + 0.5 * equal),
        ):
            values[f"{prefix} {name} return"] = weights @ mean
            values[f"{prefix} {name} volatility"] = portfolio_volatility(
                weights.tolist(), covariance.to_numpy().tolist()
            )
            values[f"{prefix} {name} bonds"] = weights.loc[sorted(RESERVE_ELIGIBLE)].sum()
        if months == 59:
            stress = select_fit(mean - 0.03, covariance)
            for field in ("return", "volatility", "mixes_qualifying"):
                values[f"all estimates cut {field}"] = stress[field]
            one_point_cuts = {}
            for ticker in mean.index:
                shocked = mean.copy()
                shocked[ticker] -= 0.01
                one_point_cuts[ticker] = select_fit(shocked, covariance)
            values["all single cuts feasible"] = all(f["found"] for f in one_point_cuts.values())
            values["XLE cut lowest return"] = min(one_point_cuts, key=lambda t: one_point_cuts[t]["return"]) == "XLE"
            values["XLE cut return"] = one_point_cuts["XLE"]["return"]
            for ticker in ("QQQ", "XLE", "LQD"):
                values[f"LQD cut {ticker} weight"] = one_point_cuts["LQD"]["weights"][ticker]
            values["base cushion"] = fit["return"] - OBJECTIVE
            values["9% objective return"] = select_fit(mean, covariance, objective=0.09)["return"]
            values["30% objective qualifying"] = select_fit(mean, covariance, objective=0.30)["mixes_qualifying"]
            floor_40 = select_fit(mean, covariance, floor=0.40)
            values["40% floor unchanged"] = floor_40["weights"].equals(target)
            floor_60 = select_fit(mean, covariance, floor=0.60)
            values["60% floor return"] = floor_60["return"]
            for ticker in ("QQQ", "XLE", "LQD"):
                values[f"60% floor {ticker} weight"] = floor_60["weights"][ticker]
        if months == 23:
            values["minimum constrained share"] = minimum_constrained_share(
                values["23 equal return"], fit["return"]
            )
            evaluation = returns.iloc[23:]
            for cost in (0, 10, 25, 50):
                constrained = evaluate(evaluation, target, cost / 10_000)
                benchmark = evaluate(evaluation, equal, cost / 10_000)
                for name, (net, risk) in (("constrained", constrained), ("equal", benchmark)):
                    values[f"{cost} bps {name} return"] = net
                    values[f"{cost} bps {name} volatility"] = risk
                values[f"{cost} bps vetoes cleared"] = constrained[0] >= OBJECTIVE and constrained[1] < benchmark[1]
    values["displayed costs clear vetoes"] = all(
        values[f"{cost} bps vetoes cleared"] for cost in (0, 10, 25)
    )
    values["all tested costs clear vetoes"] = all(
        values[f"{cost} bps vetoes cleared"] for cost in (0, 10, 25, 50)
    )
    values["24 return increase"] = values["24 return"] - values["59 return"]
    values["24 volatility decrease"] = values["59 volatility"] - values["24 volatility"]
    values["24 LQD increase"] = values["24 LQD weight"] - values["59 LQD weight"]
    values["36 LQD increase"] = values["36 LQD weight"] - values["59 LQD weight"]
    values["24 equity weight"] = 1 - values["24 reserves"]
    fits, effects = analyze(returns)
    values["attribution baseline months"] = len(returns)
    values["attribution shorter months"] = len(returns.tail(24))
    for label, swaps in CASES:
        fit = fits[swaps]
        for ticker, weight in fit["weights"].items():
            values[f"{label} {ticker} weight"] = weight
        for field in ("return", "volatility"):
            values[f"{label} {field}"] = fit[field]
    for name, row in effects.items():
        for metric, effect in row.items():
            values[f"{name} {metric} change"] = float(effect * 100)
    return values


# Each entry identifies a passage and pairs its model figures with their printed
# values in reading order. Column order distinguishes figures on the same row.
CITATIONS = {
    "driver attribution": [
        ("What drove the change", "attribution baseline months=59;attribution shorter months=24"),
        ("| 59-month baseline |", "59-month baseline QQQ weight=20%;59-month baseline XLE weight=25%;59-month baseline LQD weight=55%;59-month baseline return=8.31%;59-month baseline volatility=11.43%;59-month baseline LQD weight=55%"),
        ("| Return estimates only |", "Return estimates only XLE weight=20%;Return estimates only LQD weight=65%;Return estimates only FBMPX weight=15%;Return estimates only return=8.08%;Return estimates only volatility=10.82%;Return estimates only LQD weight=65%"),
        ("| Fund volatilities only |", "Fund volatilities only QQQ weight=20%;Fund volatilities only XLE weight=25%;Fund volatilities only LQD weight=55%;Fund volatilities only return=8.31%;Fund volatilities only volatility=8.83%;Fund volatilities only LQD weight=55%"),
        ("| Correlations only |", "Correlations only QQQ weight=25%;Correlations only XLE weight=15%;Correlations only EWZ weight=10%;Correlations only LQD weight=50%;Correlations only return=8.53%;Correlations only volatility=9.46%;Correlations only LQD weight=50%"),
        ("| 24-month answer |", "24-month answer QQQ weight=20%;24-month answer XLE weight=15%;24-month answer EWZ weight=5%;24-month answer LQD weight=60%;24-month answer return=8.79%;24-month answer volatility=6.70%;24-month answer LQD weight=60%"),
        ("| Return estimates |", "Return estimates LQD weight change=+10.00;Return estimates volatility change=-0.56;Return estimates return change=+0.00"),
        ("| Fund volatilities |", "Fund volatilities LQD weight change=+0.00;Fund volatilities volatility change=-2.55;Fund volatilities return change=+0.05"),
        ("| Correlations |", "Correlations LQD weight change=-5.00;Correlations volatility change=-1.62;Correlations return change=+0.44"),
        ("| Total |", "Total LQD weight change=+5.00;Total volatility change=-4.73;Total return change=+0.49"),
    ],
    "readme": [
        ("LQD rises from", "59 LQD weight=55%;36 LQD weight=80%"),
    ],
    "memo": [
        ("sleeve holds at least", "59 blend bonds=38.8%"),
        ("the 25/75 sleeve estimates", "59 blend return=9.58%;36 blend return=13.47%;24 blend return=12.70%;23 return=8.31%;23 blend return=3.49%"),
        ("**Changed input and result.**", "10 bps constrained return=11.34%;10 bps constrained volatility=9.45%;10 bps equal return=15.69%;10 bps equal volatility=9.96%;23 blend bonds=37.50%;23 blend return=3.49%"),
        ("LQD shift from", "59 LQD weight=55%;36 LQD weight=80%"),
    ],
    "results": [
        ("sleeve holds at least", "59 blend bonds=38.8%"),
        ("| All 59 monthly returns |", "59 blend return=9.58%;59 blend bonds=38.75%;59 blend volatility=12.90%;59 equal volatility=13.57%"),
        ("| Last 36 monthly returns |", "36 blend return=13.47%;36 blend bonds=45.00%;36 blend volatility=9.13%;36 equal volatility=9.94%"),
        ("| Last 24 monthly returns |", "24 blend return=12.70%;24 blend bonds=40.00%;24 blend volatility=8.58%;24 equal volatility=9.36%"),
        ("| Constrained | 11", "10 bps constrained return=11.34%;10 bps constrained volatility=9.45%"),
        ("| Equal weight | 15", "10 bps equal return=15.69%;10 bps equal volatility=9.96%"),
        ("The constrained fit used", "23 QQQ weight=10%;23 XLE weight=40%;23 LQD weight=50%"),
        ("| Constrained | 8", "23 return=8.31%;23 reserves=50.00%"),
        ("| Equal weight | 1.88", "23 equal return=1.88%;23 equal bonds=33.33%"),
        ("| 25/75 pilot |", "23 blend return=3.49%;23 blend bonds=37.50%"),
        ("| 50/50 blend |", "23 halfway return=5.09%;23 halfway bonds=41.67%"),
        ("Reaching 8% requires", "minimum constrained share=95.24%;0 bps constrained return=11.39%;10 bps constrained return=11.34%;25 bps constrained return=11.26%;displayed costs clear vetoes=Both replay tests passed at each cost setting"),
        ("Lower every annual return estimate", "all estimates cut mixes_qualifying=10,874;all estimates cut return=8.10%;all estimates cut volatility=12.59%"),
        ("Use the last 36 months", "59 LQD weight=55%;36 LQD weight=80%;59 volatility=11.43%;36 volatility=7.40%"),
        ("| Raise the return objective", "30% objective qualifying=No grid mix"),
        ("The separate [AI-off", "24 return=8.79%;24 volatility=6.70%;24 LQD weight=60%;24 blend return=12.70%"),
    ],
    "validation": [
        ("| Independent recalculation |", "59 mixes_tested=53,130;59 mixes_qualifying=22,829;36 mixes_qualifying=36,889"),
        ("The main weakness is window sensitivity", "59 LQD weight=55%;36 LQD weight=80%"),
        ("Base case (all 59 months", "59 QQQ weight=20%;59 XLE weight=25%;59 LQD weight=55%;59 return=8.31%;59 volatility=11.43%"),
        ("| Estimates |", "all single cuts feasible=Still feasible every time;LQD cut QQQ weight=15%;LQD cut XLE weight=30%;LQD cut LQD weight=55%;XLE cut lowest return=gives the lowest estimated return;XLE cut return=8.06%;base cushion=0.31"),
        ("| Window |", "36 XLE weight=10%;36 LQD weight=80%;36 FBMPX weight=10%;36 return=8.30%;36 volatility=7.40%;36 LQD increase=25 percentage points"),
        ("| Window (replay) |", "23 QQQ weight=10%;23 XLE weight=40%;23 LQD weight=50%;10 bps constrained return=11.34%;10 bps constrained volatility=9.45%;10 bps equal return=15.69%;10 bps equal volatility=9.96%"),
        ("| Costs |", "0 bps constrained return=11.39%;50 bps constrained return=11.12%;0 bps constrained volatility=9.44%;50 bps constrained volatility=9.52%;all tested costs clear vetoes=Both vetoes cleared at all four tested costs"),
        ("| Constraints |", "9% objective return=9.09%;30% objective qualifying=no mix qualifies;40% floor unchanged=the mix is unchanged;60% floor QQQ weight=5%;60% floor XLE weight=35%;60% floor LQD weight=60%;60% floor return=8.10%;59 LQD weight=55%"),
        ("| Qualifying mix found? |", "24 mixes_qualifying=31,774;24 mixes_tested=53,130"),
        ("| Weights |", "24 LQD weight=60%;24 TLT weight=0%;24 equity weight=40%;24 QQQ weight=20;24 XLE weight=15;24 EWZ weight=5"),
        ("| Estimated return |", "24 return=8.79%"),
        ("| Volatility |", "24 volatility=6.70%"),
        ("| Direction vs. 59-month answer", "59 return=8.31%;59 volatility=11.43%;59 LQD weight=55%;24 volatility decrease=4.73;24 LQD increase=5 points"),
        ("**What happened and why.**", "24 TLT weight=0%;59 QQQ estimate=16.0%;24 QQQ estimate=23.1%;59 FBMPX estimate=14.7%;24 FBMPX estimate=25.3%;59 LQD estimate=-0.9%;24 LQD estimate=-0.4%;59 LQD volatility=9.9%;24 LQD volatility=5.6%;59 LQD weight=55%;36 LQD weight=80%;24 LQD weight=60%"),
        ("| Constrained | 12%", "10 bps constrained return=11.34%;10 bps constrained volatility=9.45%"),
        ("| Equal weight | 14%", "10 bps equal return=15.69%;10 bps equal volatility=9.96%"),
        ("The fitted mix held", "23 LQD weight=50%;23 XLE weight=40%"),
        ("**The claim.**", "59 equal return=10.00%;59 equal bonds=33.3%"),
        ("**What I found.**", "23 equal return=1.88%;23 blend return=3.49%;minimum constrained share=95.24%"),
    ],
    "24-month record": [
        ("| Qualifying mixes |", "59 mixes_qualifying=22,829;59 mixes_tested=53,130;24 mixes_qualifying=31,774;24 mixes_tested=53,130"),
        ("| Estimated annual return |", "59 return=8.3063%;24 return=8.7948%"),
        ("| Annualized volatility |", "59 volatility=11.4256%;24 volatility=6.6991%"),
        ("| LQD + TLT |", "59 reserves=55%;24 reserves=60%"),
        ("**Prediction comparison.**", "24 return increase=0.49;24 LQD increase=5 percentage points;24 volatility decrease=4.73;59 LQD volatility=9.87%;24 LQD volatility=5.64%;24 LQD weight=60%"),
        *[(f"| {ticker} |", f"59 {ticker} weight={first};24 {ticker} weight={last}")
          for ticker, first, last in (
              ("QQQ", "20%", "20%"), ("XLE", "25%", "15%"), ("EWZ", "0%", "5%"),
              ("LQD", "55%", "60%"), ("TLT", "0%", "0%"), ("FBMPX", "0%", "0%"),
          )],
    ],
    "replay record": [
        ("The optimizer found", "23 mixes_qualifying=4,964;23 mixes_tested=53,130;23 return=8.3060%;23 volatility=17.2810%"),
        ("| Constrained mix | 11.3370%", "10 bps constrained return=11.3370%;10 bps constrained volatility=9.4545%"),
        ("| Equal weight | 15", "10 bps equal return=15.6934%;10 bps equal volatility=9.9588%"),
        ("**Pilot mandate check.**", "23 blend bonds=37.50%;23 blend return=3.4864%;23 equal return=1.88%;23 halfway return=5.09%;minimum constrained share=95%"),
    ],
    "partner swap": [
        ("| Constrained | 11.3370%", "10 bps constrained return=11.3370%;10 bps constrained volatility=9.4545%"),
        ("| Equal weight | 15.6934%", "10 bps equal return=15.6934%;10 bps equal volatility=9.9588%"),
        ("| Constrained | 11.1221%", "50 bps constrained return=11.1221%;50 bps constrained volatility=9.5217%"),
        ("| Equal weight | 15.4536%", "50 bps equal return=15.4536%;50 bps equal volatility=10.0237%"),
        ("The 25/75 blend estimated", "23 blend return=3.4864%;23 blend bonds=37.50%"),
        ("training estimate stayed", "23 blend return=3.49%"),
    ],
}


def formatted_value(key, value, cited):
    number = re.match(r"[+-]?\d[\d,]*(?:\.(\d+))?", cited)
    if number is None:
        if isinstance(value, bool):
            return cited if value else "False"
        return cited if value == 0 else str(value)
    decimals = len(number[1] or "")
    if key.endswith(" change"):
        return f"{value:+.{decimals}f}"
    if cited.endswith("%"):
        return f"{value:.{decimals}%}"
    if key.endswith((" increase", " decrease", " cushion")):
        return f"{value * 100:.{decimals}f}" + cited[number.end():]
    if key.endswith(" weight"):
        return f"{value * 100:.{decimals}f}"
    return f"{value:,.{decimals}f}"


def audit(values, overrides=None, only=None):
    failures = []
    total = 0
    for document, groups in CITATIONS.items():
        if only is not None and document != only:
            continue
        path = (overrides or {}).get(document, ROOT / DOCUMENTS[document])
        try:
            raw = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raw = ""
        # A passage ends at the next Markdown table row or paragraph.
        passages = re.split(r"\n\s*\n|\n(?=\|)", raw)
        for anchor, entries in groups:
            claims = [entry.split("=", 1) for entry in entries.split(";")]
            matches = [re.sub(r"\s+", " ", passage) for passage in passages if anchor in passage]
            passage = matches[0] if len(matches) == 1 else ""
            cursor = 0
            for key, cited in claims:
                pattern = re.escape(cited)
                if re.match(r"[+-]?\d", cited):
                    pattern = r"(?<![\d.,+-])" + pattern + r"(?![\d]|[.,]\d)"
                match = re.search(pattern, passage[cursor:])
                if match:
                    cursor += match.end()
                recomputed = formatted_value(key, values[key], cited)
                passed = match is not None and recomputed == cited
                if not passed:
                    failures.append((document, anchor, key))
                print(f"{'PASS' if passed else 'FAIL'} | {key} | cited {cited} | "
                      f"recomputed {recomputed} | {path if overrides else DOCUMENTS[document]}")
                total += 1
    return total, failures


def self_test(values):
    document = "validation"
    path = ROOT / DOCUMENTS[document]
    original = path.read_text(encoding="utf-8")
    before = "estimated 8.31% return at 11.43% volatility"
    if original.count(before) != 1:
        print("FAIL: self-test could not identify the base-case citation.")
        return 1
    with TemporaryDirectory() as directory:
        copy = Path(directory) / path.name
        copy.write_text(original.replace(before, before.replace("8.31%", "8.32%")),
                        encoding="utf-8")
        _, failures = audit(values, {document: copy}, only=document)
    expected = [(document, "Base case (all 59 months", "59 return")]
    if failures != expected:
        print(f"FAIL: self-test expected exactly one changed citation, got {failures!r}")
        return 1
    print("PASS: self-test caught the change from 8.31% to 8.32%.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    values = model_values()
    if args.self_test:
        return self_test(values)
    total, failures = audit(values)
    print(f"{total - len(failures)}/{total} claims pass.")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
