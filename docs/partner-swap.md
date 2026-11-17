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

Pending a GitHub publication of this pre-run prediction. Record both portfolios' realized metrics, both vetoes, the committee decision and why the observed result did or did not match the prediction.
