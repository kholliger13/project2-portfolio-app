# AI Finance | Lab 13–19 review

Kayla Holliger · FIN 43900 · Purdue

**Proposed committee decision: approve the frozen data for a classroom demonstration and hold PAYEMS admission to Project 2.** The historical checks establish what is visible in the captured vintages at a date cutoff. A trading or portfolio decision requires additional evidence.

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

Stop each Streamlit server with Ctrl+C. Keep the default historical dates and avoid the refresh button for the frozen rates demo. Uncached or refreshed vintages need internet access. `prices.csv` is the frozen Lab 14 input.

## Work and evidence

| Work | Implementation and evidence |
|---|---|
| Lab 13 | [Meridian baseline write-up](evidence/Lab13_meridian_baselines.md), [baseline script](lab13_baselines.py), [common case](evidence/meridian_foundation_common_case.md) |
| Lab 14 | [Portfolio app](app.py), [shared engine](portfolio.py), [window comparison](evidence/Lab14_portfolio_app_2026_10_22.md), [reviewer regression check](verify_portfolio_app.py) |
| Lab 15 | [Classroom fixture and decisions](Lab15_known_answer_provenance_2026_03_31.md), [gate](asof.py), [PAYEMS vintage reconstruction](payems_point_in_time.py), [individual submission](evidence/Lab15_KaylaHolliger_individual_submission.md) |
| Later work | [Current-versus-as-of explorer](asof_app.py), [PAYEMS data card](evidence/PAYEMS_data_card_2026_10_29.md), [rates app](rates_app.py), [Project 2 review](evidence/Rates_app_Project2_review_2026_10_29.md). The available materials do not establish the individual Lab 16–19 assignments or completion. |

Read the [claim and decision](DECISION.md), [SR 26-2 model validation review](MODEL_VALIDATION.md), [three video briefs](VIDEOS.md), and [frozen must-fix list](MUST_FIX.md). Historical write-ups retain their original paths and instructions. Use the commands above for this checkout.

Educational work with AI assistance. The Meridian and classroom fixtures use supplied training inputs.
