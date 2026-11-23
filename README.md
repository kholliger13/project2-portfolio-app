# AI Finance | Lab 13–19 review

Kayla Holliger · FIN 43900 · Purdue

I used OpenAI Codex to implement, test and document the app and replay, and Claude
(Anthropic) to review my plan, draft two predictions at my request (the 23/36 replay and
the 50 bp cost check), and run one cold run. I wrote the Locked Changed-Input Record
prediction (24-month window) myself, without AI. The analysis and the decision are mine.
Education, not investment advice.

**Portfolio committee decision: pilot 25% constrained and 75% equal weight, rebalanced monthly to fixed targets.** The funded sleeve clears the 8% screen on the decision-date estimates. Consider expanding toward 50% only after six months of live results clear both replay vetoes. [Committee decision and triggers](docs/decision-memo.md#portfolio-pilot-decision) · [Historical replay](LOCKED_CHANGED_INPUT.md)

PAYEMS is the project’s point-in-time signal, used as a monitoring trigger: if the point-in-time payroll change is negative for two consecutive months, the pilot goes back to the committee. [Data card](evidence/PAYEMS_data_card_2026_10_29.md) · [PAYEMS decision](docs/decision-memo.md#payems-data-decision)

## Run from a clean checkout

From the repository root, use Python 3.13 (tested on 3.13.15). Install dependencies once. The review checks and the two demos below use bundled inputs after installation and require no API key.

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
sh review.sh && python replay.py
```

The last command prints the three Meridian baselines, then verifies both portfolio windows, the classroom provenance and signal answers, the PAYEMS source and cutoff cases, and both rates interfaces. It then prints the portfolio replay, funding checks, and cost stress. An error stops the run. During these automated checks, Streamlit may print `missing ScriptRunContext` or `No runtime found` warnings. These are expected when the checks finish successfully.

| Demo | Command | What to reproduce |
|---|---|---|
| Portfolio | `python -m streamlit run app.py` | Keep the six-fund CSV, 8% objective and 20% reserve floor. Switch from **All returns** to **Last 36 months**. LQD rises from 55% to 80%. Scroll to **Mandate verdicts** for the two baselines and constrained mix. |
| Rates and PAYEMS | `python -m streamlit run rates_app.py` | Start on October 4, 2024 with same-day releases excluded. In the PAYEMS tab, toggle same-day releases to see a comparison. For the next-day monitoring signal, clear the Rates selection before changing the date to October 5. For a negative reading, enter the actual previous month’s committee decision date to evaluate the two-month trigger. |
| Live comparison, optional | `python -m streamlit run asof_app.py` | Compare current FRED data with a historical ALFRED vintage. The app requires internet access. Its test in `review.sh` uses controlled responses. |

Stop each Streamlit server with Ctrl+C. Keep the default historical dates and avoid the refresh button for the frozen rates demo. Uncached or refreshed vintages need internet access. `prices.csv` is the frozen input for the six-fund portfolio app.

## Portfolio mandate and stress demo

The six-fund sleeve uses QQQ, XLE, EWZ, LQD, TLT and FBMPX. The objective is minimum estimated annualized volatility on the 5-point grid, with at least 8% estimated annual return and at least 20% combined in LQD and TLT. Weights are fully invested and long-only. Equal weight is the comparison benchmark, with inverse volatility as the second transparent baseline. The 8% screen applies to the funded sleeve using estimates available at the decision date. The replay provides historical evidence on the constrained allocation. The Meridian training case is a separate app mode.

In the portfolio app, change the estimation window, edit a return estimate, or raise the return objective to 30% with the bundled defaults. Read each verdict and the stop message when no mix satisfies both screens. The replay command varies costs at 0, 10 and 25 basis points on the same fixed targets. The locked result uses 10 basis points.

## Work and evidence

This mapping follows the Week 12 handout and the linked official lab prompts. Earlier filenames retain their original labels.

| Project 2 component | Studio mapping | Available evidence |
|---|---|---|
| Mandate, hard constraints and client question | Lab 13 and your own mandate | [Meridian common case](evidence/meridian_foundation_common_case.md), [mandate checker](mandate.py). See the six-fund mandate above and the [committee decision](docs/decision-memo.md). |
| Baselines and mandate check | Lab 14 | [Meridian baselines](evidence/Lab13_meridian_baselines.md), [baseline script](lab13_baselines.py) |
| Portfolio app, constrained search and stress run | Lab 15 | [App](app.py), [shared engine](portfolio.py), [window comparison](evidence/Lab14_portfolio_app_2026_10_22.md), [verification](verify_portfolio_app.py). See the [stress results and stop conditions](docs/validation-and-ai-use.md#3-stress-run). |
| Provenance gate and classroom known answer | [Lab 16](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-16-provenance-gate.md) | [Gate](asof.py), [all 12 row dispositions and financial sanity checks](Lab15_known_answer_provenance_2026_03_31.md), [known-answer test](verify_asof.py), [partner date-shift proof](evidence/partner_asof_date_shift_proof.txt) |
| Live point-in-time audit, data card and series decision | [Lab 17](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-17-point-in-time.md) | [Live app](asof_app.py), [October 5 known answer](evidence/asof_known_answer_2026_10_05.md), [PAYEMS revision probe](evidence/payems_app_probe_2025_01_15.md), [data card](evidence/PAYEMS_data_card_2026_10_29.md), [series decision](docs/decision-memo.md#payems-data-decision). The data card also records the publication-date challenge and response. |
| Buffett skill, COST known answer, missing-data and unsupported-number probes | [Lab 18](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md) | [Saved checkout verification](evidence/week11/verification_status.md) and [COST decision](evidence/week11/reports/COST_decision.md). These are archived Week 11 evidence. |
| Buffett, Cathie Wood and Burry panel on shared 10-K facts | [Lab 19](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md) | [COST benchmark, threshold probe, Apple panel and conditional screening decision](evidence/week11/Lab_2026_11_05.md) and [verification](evidence/week11/panel_verification_2026_11_05.md). Saved bull/bear notes cover COST and JPM. An Apple-specific partner exchange is unresolved. |
| Locked Changed-Input Record | Lab 11 pattern, applied to one Project 2 input | [AI-off 24-month prediction and result](docs/locked-record-24-month.md). The prediction was verified on GitHub before the run. The [23/36 historical replay](LOCKED_CHANGED_INPUT.md) and [50 bp cost check](docs/partner-swap.md) are supporting evidence. |
| Submission bundle | Project 2 page and submission architecture | [Submission manifest](docs/submission-manifest.md), [published README](https://github.com/kholliger13/project2-portfolio-app/blob/main/README.md), and [completed partner cold run](docs/partner-swap.md). Video and transcript links remain unresolved. |

Read the [claim and decision](docs/decision-memo.md), [SR 26-2 model validation review](MODEL_VALIDATION.md), [three video briefs](VIDEOS.md), and [frozen must-fix list](MUST_FIX.md). Historical write-ups retain their original paths and instructions. Use the commands above for this checkout.

Educational work with AI assistance. The Meridian and classroom fixtures use supplied training inputs.

See [visible output](docs/results.md), [validation and AI use](docs/validation-and-ai-use.md), and the [submission manifest](docs/submission-manifest.md).
