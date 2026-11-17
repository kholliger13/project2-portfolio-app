# PAYEMS data card — Kayla Holliger

**Download date:** October 29, 2026. **Series ID:** PAYEMS.

**Source and link:** U.S. Bureau of Labor Statistics (BLS), Current Employment Statistics establishment survey; distributed by the Federal Reserve Bank of St. Louis through [FRED PAYEMS](https://fred.stlouisfed.org/series/PAYEMS) and historical [ALFRED PAYEMS vintages](https://alfred.stlouisfed.org/series?seid=PAYEMS).

**What it measures:** The level of U.S. nonfarm payroll employment. Jobs at different establishments are counted separately for a person with multiple jobs. This is an employment level, not the monthly change in jobs and not an interest rate. [BLS survey definitions](https://www.bls.gov/web/empsit/cesfaq.htm).

**Units and frequency:** Thousands of persons, seasonally adjusted, monthly. For example, 159,044 means about 159.044 million payroll jobs. A date such as 2026-09-01 labels September, not a September 1 release. [FRED series definition](https://fred.stlouisfed.org/series/PAYEMS).

**Publication lag:** Preliminary estimates generally arrive early in the following month, about three weeks after the reference pay period containing the 12th. Actual release dates govern eligibility; do not assume a fixed lag. [BLS release and revision FAQ](https://www.bls.gov/web/empsit/cesfaq.htm). In the saved ALFRED prework, September 2026 first appears in the October 2 vintage: two calendar days after September ended, and 31 days after its September 1 label. It was absent at September 30. This establishes date-level availability; the CSVs do not verify an intraday trading timestamp.

**Revisions:** Yes. BLS revises initial estimates in the next two monthly releases and incorporates annual benchmark and seasonal-adjustment updates. [BLS revisions explanation](https://www.bls.gov/web/empsit/cesfaq.htm). Use the eligible historical vintage at each decision, rather than today’s revised values.

## App exercise: last month-end versus today

Ran the real `asof_app.py` through Streamlit AppTest with PAYEMS in the additional-ID box. Both runs used live public CSV downloads, not substituted data. The four class rates remained selected.

ALFRED labeled the PAYEMS snapshot returned for the 2026-10-29 request as 2026-10-28. The app displays this returned date. In this check its values match the current FRED file; no later information is inferred from the earlier label.

| Series | As known on | Latest measured period known then | Value known then | Newer values in current data | Revised shared values |
|---|---|---|---:|---:|---:|
| PAYEMS | 2026-09-30 | 2026-08-01 | 159,075.00 | 1 | 2 |
| PAYEMS | 2026-10-29 | 2026-09-01 | 159,044.00 | 0 | 0 |
| DGS10 | 2026-09-30 | 2026-09-29 | 5.26 | 20 | 0 |
| DGS10 | 2026-10-29 | 2026-10-28 | 5.05 | 0 | 0 |

**Values that vanish at the earlier cutoff:** September 2026. These measured months have no nonmissing value in the September 30 information set and must not be supplied from today’s file. Older months may remain present but have revised values.

**PAYEMS revision result:** 2 shared observations differ between the month-end vintage and today. Counts cover the full downloaded history, not just the chart window. A zero count in the today-versus-today run does not mean PAYEMS is never revised; those downloads describe the same information date.

**Daily market-rate comparison:** DGS10 has 0 revised shared observations in this comparison. It shows almost no publication lag relative to monthly payrolls; weekends, holidays and the daily release time still matter. No revisions were detected over this comparison; that is an observed result, not a guarantee against future corrections.

**Use in Project 2:** PAYEMS is a revised, lagged economic series. It is suitable for point-in-time exploration only with the eligible vintage at each decision and adequate coverage. This exercise does not establish the unseen Project 2 eligibility rules or predictive value.

## Reproduce and evidence

Run `.venv/bin/python verify_payems_month_end.py` from the course folder.

- [Current FRED CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS)
- [Month-end ALFRED CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2026-09-30)
- [Today ALFRED CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2026-10-29)

AI assistance: Codex helped run the app exercise, compare downloaded values, and draft this course data card.

I trust publication date least because the app’s October 29 PAYEMS request returned an ALFRED snapshot labeled October 28, and the CSV does not give an exact publication time for each observation. The app directly detected two revised observations since September 30, while the [FRED PAYEMS page](https://fred.stlouisfed.org/series/PAYEMS) explicitly identifies the units as thousands of persons, so revisions and units have clearer evidence than availability before a particular trade.

**Project 2 decision — Quarantine:** PAYEMS is published after the measured month and revised in the next two monthly releases and through annual benchmark and seasonal-adjustment updates; the app showed December 2024 at 159,536 in the January 15, 2025 vintage versus 158,316 today (thousands of persons). Admit only if Project 2 permits this economic input and each decision uses the eligible historical vintage with verified availability before the trade, sufficient sample coverage, and a documented cutoff convention; never use today’s revised values with a fixed lag as a substitute.

## Final verification — October 29, 2026

- The local Streamlit app is running; its health endpoint returned `ok`. PAYEMS is prefilled in the additional-series box alongside the four selected class rates.
- [October 5 known-answer proof](asof_known_answer_2026_10_05.md): all four measured dates and values match (BAA 6.47, FEDFUNDS 3.75, DGS10 5.28, MORTGAGE30US 7.28).
- [January 15 PAYEMS probe](payems_app_probe_2025_01_15.md): December 2024 was 159,536 then versus 158,316 today; 381 shared observations were revised. Both live checks passed again on the final app through Streamlit AppTest.
- Automated checks passed for default controls, custom IDs, unknown-ID isolation, missing values, revision counts, cache behavior, and rejection of future returned vintages.
- This card contains the source, measurement, units, publication lag, revision behavior and download date, followed by the two-sentence publication-date answer and the quarantine decision with conditions for admission.
