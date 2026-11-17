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

README handoff gap: the shared link needs to resolve directly to Zachary's Project 2 README in the published branch. No substitute app was run and no coaching was given. The reciprocal run on Kayla's repository is pending.

## Pre-run cost prediction for Kayla's portfolio

Prediction prepared with OpenAI Codex before testing the new cost. This is a separate stress check from the original locked replay.

| Item | Pre-run prediction |
|---|---|
| Changed input | Increase one-way trading cost from **10 to 50 basis points per dollar traded**, including the initial purchase for both portfolios. |
| Fixed inputs | Keep the same 23-month fit, 36-month evaluation, two portfolios, target weights, and rebalance schedule. |
| Expected movement | Both portfolios' annualized net returns should fall. Annualized volatility could move slightly in either direction because turnover costs vary by month. I expect the constrained mix to remain less volatile. |
| Expected vote | Expect both replay vetoes to stay clear. Funding should remain on hold pending confirmation of the 8% screen's scope, since changing replay costs leaves training estimates and blend weights unchanged. |

### Before output at 10 bps

Source: the [previously recorded replay](../LOCKED_CHANGED_INPUT.md), committed at `159bf56`.

| Portfolio | Annualized net return | Annualized volatility |
|---|---:|---:|
| Constrained | 11.3370% | 9.4545% |
| Equal weight | 15.6934% | 9.9588% |

Both vetoes cleared. The 25/75 blend estimated 3.4864% return and held 37.50% in LQD and TLT.

### After output at 50 bps

Pending a GitHub publication of this pre-run prediction. Record both portfolios' realized metrics, both vetoes, the committee decision and why the observed result did or did not match the prediction.
