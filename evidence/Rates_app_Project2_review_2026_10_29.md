# Rates app and Project 2 series review — October 29, 2026

Working path confirmed: `/Users/kaylaholliger/Documents/Courses/AIFinance2026/KaylaHolliger`.

## Run the local app

```sh
cd /Users/kaylaholliger/Documents/Courses/AIFinance2026/KaylaHolliger
.venv/bin/python -m streamlit run rates_app.py
```

The existing portfolio `app.py` remains available. The new app has a rates explorer, the frozen 10/27 PAYEMS series, and a provisional Project 2 review.

Today's supplied classroom defaults: BAA (monthly Moody's Baa corporate yield), FEDFUNDS (monthly effective federal funds), DGS10 (daily 10-year Treasury), MORTGAGE30US (weekly mortgage rate, ending Thursday). PAYEMS remains the prework series on its own tab, with its FRED link. DGS2 and DFF remain optional daily series. FEDFUNDS is used explicitly for the assigned monthly series; DFF is not substituted for it.

Charts retain native frequencies, without daily filling or interpolation. Monthly labels identify measured months, not release dates. Rates are annual percentages; the optional 10-year minus 2-year spread is in percentage points, using only dates where both series have a value. The supplied list explicitly includes the student's chosen prework series; this supports keeping PAYEMS in today's exercise, but does not establish its admission to Project 2.

To view live-source data, select today's decision date and click **Refresh selected vintages from ALFRED**. This replaces the selected snapshots with a fresh retrieval and records its time. Retrieval establishes the information returned at that time, not what was available earlier within the day. The PAYEMS prework tab intentionally retains the original 10/27 evidence.

Choose any supported historical decision date and observation start. The app requests that date's ALFRED vintage, never today's values filtered only by observation date. Excluding same-day publications requests the previous calendar day's vintage. This conservative convention does not reconstruct an exact trading timestamp or distinguish individual releases within a day.

ALFRED snapshot dates establish the requested historical information set. They do not establish each row's first-publication date. Source CSVs, URLs, retrieval times, and SHA-256 integrity hashes are saved in `rates_source_vintages/`. Missing rates remain missing. Source failures are visible; there is no fallback to current values or invented data. Uncached dates require internet access and successful ALFRED responses. The default October 4, 2024 and previous-day examples are cached.

Official sources: [ALFRED DGS10 historical download](https://alfred.stlouisfed.org/series/downloaddata?seid=DGS10), [FRED real-time periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html), [FRED observations documentation](https://fred.stlouisfed.org/docs/api/fred/series_observations.html).

## Provisional Project 2 decision

**HOLD for final admission pending the actual Project 2 instructions.** No assignment-specific permission is inferred from the technical checks.

The 10/27 real-data series located in this workspace is PAYEMS: monthly seasonally adjusted nonfarm employment levels, in thousands of persons. It is a candidate economic input with captured historical revisions. If Project 2 requires an interest-rate series, PAYEMS does not meet that requirement. If economic predictors are permitted, it may qualify once the required sample, decision timing, transformations, and verification rules are established.

Saved coverage is August 2024–September 2026, with 25 ALFRED vintage dates through October 2, 2026, retrieved October 27: 91 changed-value/initial-publication records and 336 snapshot rows. This does not establish earlier history, later revisions, or exact intraday availability. A first appearance within captured history is evidence of availability in that capture, not proof of an independently verified original BLS release timestamp.

The independent classroom fixture passed the known-answer test. That fixture certifies the exercise's expected filtering behavior; it is not a PAYEMS or Project 2 market-data answer key. `payems_verify.py` retains a pending instructor-key message from its original scope; the classroom key was subsequently completed separately in `verify_asof.py`. Neither constitutes an unseen Project 2 key.

PAYEMS technical evidence supports date-based exploration within coverage. It does not establish predictive usefulness, portfolio benefits, assignment eligibility, or financial validity by itself. A proposed trading predictor must use the eligible vintage at each decision, with transformations computed after selection and without future releases. Required sample length and out-of-sample evaluation remain assignment-dependent.

## Verification

```sh
.venv/bin/python verify_asof.py
.venv/bin/python payems_verify.py
.venv/bin/python verify_rates_app.py
```

Verified: classroom row dispositions and signal values; three PAYEMS source-row comparisons; seven historical date/boundary cases; shuffled input; conflicting publications; historical DGS10 October 4 vintage ending with October 3 at 3.85%; previous-day vintage selection; preservation of missing values; rejection of wrong vintage headers, HTML, duplicate dates, and nonfinite values; Streamlit default, same-day exclusion, and empty-selection flows. App tests exercise rendered Streamlit elements, not a screenshot-based browser review.

AI assistance: Codex helped build the application, retrieve archive examples, run checks, and draft this review for FIN 43900. Final assignment requirements and student judgment remain to be supplied.
