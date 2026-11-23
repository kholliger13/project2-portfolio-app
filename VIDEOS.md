# Three recording briefs

Open each recording with both statements. Update the disclosure to reflect what you actually used for the recording.

> I used OpenAI Codex to implement, test, and document the app and replay. I used Claude (Anthropic) to review my plan, draft the 23/36 replay and 50 bp cost predictions at my request, and run one cold run. I wrote the 24-month Locked Changed-Input Record prediction myself with AI off.
>
> The analysis and decision are mine. Education, not investment advice.

## 1. How it changed

**Maximum length:** 3:00. **Audience:** Course reviewer. **Show:** The baseline table, then the two portfolio windows side by side.

- Start with Lab 13. The benchmark clears the 6.5% modeled return objective and misses the 3% reserve floor. The other two baselines clear the floor and miss the return objective.
- Move to Lab 14. Keep its separate 8% objective and 20% reserve floor fixed. Switch from all 59 monthly returns to the last 36. LQD rises from 55% to 80%.
- Close with the change in the work. A static baseline comparison became an app that makes the assumptions and sensitivity visible. The vintage work later added a check on which inputs were knowable on the decision date. Use the [documented Claude fallback check](docs/validation-and-ai-use.md#7-one-ai-output-i-checked) to explain what you checked and what changed in your thinking.

## 2. Technical walkthrough

**Maximum length:** 5:00. **Audience:** A reviewer reproducing the result. **Show:** README, terminal checks, source CSVs and the PAYEMS control.

- Trace `app.py` through `portfolio_core.py` to `portfolio.py`. Show how the selected window turns prices into monthly returns and how the grid search applies the return and bond-floor screens before choosing the lowest-volatility qualifying mix.
- Run `sh review.sh`. Pause at the classroom known answer and point out why April publications are excluded from the March 31 signal.
- Open the September 6 and October 4 PAYEMS sources. In the rates app, show that the October 4 decision has no monitoring signal. Toggle same-day releases to show the +254 thousand jobs comparison. Restore the previous-day rule, clear Rates and move to October 5 to show when that reading becomes eligible for monitoring.
- Point to the two fixed expectations in `payems_verify.py`. End with the date-level limit of the captured evidence.

## 3. Committee decision

**Maximum length:** 5:00. **Audience:** An investment committee. **Show:** Start with the portfolio app running live and deliver the opening statements over the app. Show the mandate verdicts, then move to the decision and triggers.

- Ask the committee to approve a 25% constrained and 75% equal-weight pilot, rebalanced monthly to fixed targets. The funded blend clears the 8% estimated return screen on the 59-month decision-date inputs (9.58%). Consider expansion toward 50% only after six months of live results clear both replay vetoes.
- Show the 23-month fit and 36-month holdout as historical evidence. The constrained mix earned 11.34% annualized net at 9.45% volatility, clearing both vetoes. The 25/75 blend estimated 3.49% on the training period alone. Explain which estimates the actual funding decision uses.
- Return to committee if a proposed fund weight moves more than 15 percentage points, the funded sleeve falls below the 8% return screen or 20% LQD + TLT floor, or PAYEMS is negative for two consecutive months using each decision's prior-day vintage. At six months, review a constrained net return under 8% annualized or volatility at least as high as equal weight's. If the funded mandate or live performance test fails, revert to equal weight only if it passes the mandate at that re-estimate.

Add each YouTube link and its transcript location to the submission manifest after verifying the recording and transcript are accessible to the reviewer.
