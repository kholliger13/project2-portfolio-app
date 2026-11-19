# Project 2 partner swap

## Partner cold-run record

| Item | Record |
|---|---|
| Partner link | [ZacharyAlvin on GitHub](https://github.com/kholliger13/MD-A-research/tree/main/ZacharyAlvin) |
| Checkout | Fresh clone into `project2-zachary-cold-check`. The clone used `origin/main` at `07e1c52da9ddd379079b71ebf7c386460693a7bf`. |
| Commands | `GIT_TERMINAL_PROMPT=0 git clone https://github.com/kholliger13/MD-A-research.git project2-zachary-cold-check`, then from the clone root, `cd ZacharyAlvin && ls README.md`. |
| First failure | `cd: no such file or directory: ZacharyAlvin`. The partner folder was absent from the cloned main branch. |
| Elapsed time | No result reached. The clone command took about 0.44 seconds of execution time and the folder check took 0.001 seconds. |
| Result location | Unavailable. No partner README or result was reached. |

README handoff gap: the shared link needs to resolve directly to Zachary's Project 2 README in the published branch. No substitute app was run and no coaching was given.

## Zachary’s reciprocal cold-run report

| Item | Zachary’s report |
|---|---|
| Published commit reached | `0b52dcc` on `main` |
| Command | None |
| First failure | The shared KaylaHolliger folder and README were missing at that commit. |
| Elapsed time | Under 0.01 seconds for the README lookup, excluding checkout. |
| Result location | No app output was produced. |

Zachary requested the current README link so he can rerun using that link alone. A fresh fetch of the supplied GitHub repository reached `07e1c52` on `origin/main`. That commit contains the KaylaHolliger folder, and the Project 2 README and runnable bundle are still missing. The local publication fix adds both. A rerun can start once that fix is published.

## Zachary’s clean GitHub rerun

| Item | Zachary’s report |
|---|---|
| Link | [Project 2 repository](https://github.com/kholliger13/project2-portfolio-app) |
| Checkout | Fresh clone in an empty folder. `main` at [`ba706d9`](https://github.com/kholliger13/project2-portfolio-app/commit/ba706d9cf56889caf5cc8e7753b880eb12c1ce97), November 17, 2026 at 17:59:40 Eastern. |
| Commands | `git clone https://github.com/kholliger13/project2-portfolio-app`, then from the clone root, `python3.13 -m venv .venv`, `source .venv/bin/activate`, `python -m pip install -r requirements.txt`, and `sh review.sh && python replay.py`. |
| First failure | None. Exit code 0 under Python 3.13.18. |
| Elapsed | About 32 seconds from clone to the final replay line, including environment creation and installation. |
| Result | Terminal output from `python replay.py` confirmed both vetoes cleared. The funding hold was in the [README](../README.md) and [decision memo](decision-memo.md). |

No code fix was needed after the successful rerun. Publishing the standalone repository resolved the missing README. The README now explains the expected Streamlit warnings raised during automated review.

## Pre-run cost prediction for Kayla's portfolio

Kayla supplied this prediction before running the 50 bp stress check. The original locked replay remains the 10 bp baseline.

| Item | Pre-run prediction |
|---|---|
| Input | Trading cost per dollar traded |
| Old value | 10 bps (0.10%) |
| New value | 50 bps (0.50%) |
| Fixed inputs | Same 23-month fit, 36-month evaluation, target weights, and monthly rebalance schedule. Charge both portfolios for the initial purchase. |
| Expected direction | Both portfolios' annualized net returns fall. Volatility is essentially unchanged. Approximate return drop is annual turnover × 0.40 percentage points, likely under 0.5 percentage points per year. |
| Expected effect on the decision | Both vetoes stay clear unless the constrained net return starts within about 0.5 percentage points of 8%. The recorded 10 bp return was 11.3370%, or 3.3370 percentage points above 8%. The 3.49% sleeve estimate is gross and remains unchanged when only trading cost changes. |
| Expected vote | Hold pending scope. Fund a 25% constrained and 75% equal-weight pilot only if the committee confirms the 8% screen applies to the constrained allocation alone and the remaining mandate checks pass. If the screen applies to the full sleeve, reject the proposal. The 25/75 blend estimates 3.49%, and the minimum constrained share is about 95.24%. |

### Before output at 10 bps

Source: the [previously recorded replay](../LOCKED_CHANGED_INPUT.md), committed at `159bf56`.

| Portfolio | Annualized net return | Annualized volatility |
|---|---:|---:|
| Constrained | 11.3370% | 9.4545% |
| Equal weight | 15.6934% | 9.9588% |

Both vetoes cleared. The 25/75 blend estimated 3.4864% return and held 37.50% in LQD and TLT.

### After output at 50 bps

Zachary reported the run on published commit `ba706d9` after the prediction was online. The results were reproduced locally using the same `replay.evaluate()` with `trade_cost=0.005`, the original fit and evaluation dates, and the same target weights.

| Portfolio | Annualized net return | Annualized volatility | Net return change |
|---|---:|---:|---:|
| Constrained | 11.1221% | 9.5217% | −0.2149 percentage points |
| Equal weight | 15.4536% | 10.0237% | −0.2398 percentage points |

**Prediction check.** Both net returns fell by less than half a percentage point. Volatility rose about 0.07 percentage points in each portfolio. Equal weight had higher annualized one-way turnover in this replay, 51.77% versus 48.20% including initial purchases, consistent with its larger net return decline. Neither veto triggered. The constrained return remained 3.12 percentage points above 8%, and its volatility remained below equal weight’s. The 25/75 blend’s training estimate stayed at 3.49% because the fit excludes transaction costs.

**Committee line.** Pilot 25% constrained and 75% equal weight, rebalanced monthly. Expand toward 50% only after six live months clear both replay vetoes. If the funded sleeve fails the 8% return or 20% bond screen, or the six-month results fail either veto, reject the process and revert to equal weight if it passes the mandate at that re-estimate. [Full triggers and reversal](decision-memo.md#portfolio-pilot-decision)
