# AI Finance | Lab 13–19 review

Kayla Holliger · FIN 43900 · Purdue

AI assisted with repository assembly and validation. This work is for education, not investment advice.

**Portfolio committee decision: keep pilot funding on hold until the mandate scope is confirmed.** The constrained mix passed the historical replay. If the 8% screen applies to the whole sleeve, both the proposed 25/75 pilot (3.49%) and the equal-weight fallback (1.88%) fail on the 23-month estimates. [Committee decision](DECISION.md#portfolio-pilot-decision) · [Locked prediction and replay](LOCKED_CHANGED_INPUT.md)

The frozen PAYEMS data are approved for classroom demonstration. PAYEMS admission to Project 2 remains on hold pending eligibility and decision-use evidence. [PAYEMS decision](DECISION.md#payems-data-decision)

## Run from a clean checkout

From the repository root, use Python 3.13 (tested on 3.13.15). Install dependencies once. The review checks and the two demos below use bundled inputs after installation and require no API key.

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
sh review.sh
```

The last command prints the three Meridian baselines, then verifies both portfolio windows, the classroom provenance and signal answers, the PAYEMS source and cutoff cases, and both rates interfaces. An error stops the run.

| Demo | Command | What to reproduce |
|---|---|---|
| Portfolio | `python -m streamlit run app.py` | Keep the six-fund CSV, 8% objective and 20% reserve floor. Switch from **All returns** to **Last 36 months**. LQD rises from 55% to 80%. |
| Rates and PAYEMS | `python -m streamlit run rates_app.py` | Use the default October 4, 2024 cutoff. In the PAYEMS tab, compare the default date with and without same-day publications. |
| Live comparison, optional | `python -m streamlit run asof_app.py` | Compare current FRED data with a historical ALFRED vintage. The app requires internet access. Its test in `review.sh` uses controlled responses. |

Stop each Streamlit server with Ctrl+C. Keep the default historical dates and avoid the refresh button for the frozen rates demo. Uncached or refreshed vintages need internet access. `prices.csv` is the frozen input for the six-fund portfolio app.

## Work and evidence

The Week 12 handout supplies the mapping below. Earlier filenames retain their original labels.

| Project 2 component | Studio mapping | Available evidence |
|---|---|---|
| Mandate, hard constraints and client question | Lab 13 and your own mandate | [Meridian common case](evidence/meridian_foundation_common_case.md), [mandate checker](mandate.py). Confirm the final client question and mandate. |
| Baselines and mandate check | Lab 14 | [Meridian baselines](evidence/Lab13_meridian_baselines.md), [baseline script](lab13_baselines.py) |
| Portfolio app, constrained search and stress run | Lab 15 | [App](app.py), [shared engine](portfolio.py), [window comparison](evidence/Lab14_portfolio_app_2026_10_22.md), [verification](verify_portfolio_app.py). Confirm the final product's mandate verdicts and required stress run against the Project 2 instructions. |
| Point-in-time rule and data card | Labs 16 and 17 | [Classroom fixture](Lab15_known_answer_provenance_2026_03_31.md), [gate](asof.py), [PAYEMS reconstruction](payems_point_in_time.py), [data card](evidence/PAYEMS_data_card_2026_10_29.md), [rates app](rates_app.py) |
| Locked Changed-Input Record | Lab 11 pattern, applied to one Project 2 input | [Pre-run prediction and replay result](LOCKED_CHANGED_INPUT.md), [replay script](replay.py). The GitHub pre-run link remains unresolved. |
| Submission bundle | Project 2 page and submission architecture | [Week 12 studio notes](STUDIO.md). Final manifest and delivery links are unresolved. |

Read the [claim and decision](DECISION.md), [SR 26-2 model validation review](MODEL_VALIDATION.md), [three video briefs](VIDEOS.md), and [frozen must-fix list](MUST_FIX.md). Historical write-ups retain their original paths and instructions. Use the commands above for this checkout.

Educational work with AI assistance. The Meridian and classroom fixtures use supplied training inputs.
