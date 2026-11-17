# PAYEMS point-in-time filter — October 27, 2026

Working path confirmed: `/Users/kaylaholliger/Documents/Courses/AIFinance2026/KaylaHolliger`.

The filter is built and passes historical source checks. **The instructor's decision date and known-answer fixture have not been supplied. Matching that assigned answer remains pending.** The October 4, 2024 example below is an explicitly chosen historical demonstration.

## Data and series choice

Series: All Employees, Total Nonfarm (PAYEMS). Monthly, seasonally adjusted, thousands of persons. Values are employment levels, not monthly job changes.

My reason for choosing PAYEMS is that employment news can affect growth and interest-rate expectations relevant to QQQ, XLE, EWZ, LQD, TLT and FBMPX. This is an economic rationale for studying the series, not a tested claim that it predicts all six funds or that their responses have a fixed direction.

Source: [ALFRED PAYEMS download page](https://alfred.stlouisfed.org/series/downloaddata?seid=PAYEMS). Retrieved October 27, 2026; the saved page is `alfred_download_page.html`.

The observation window is August 2024–September 2026: 26 consecutive measured months. All 25 vintage dates listed by ALFRED from September 6, 2024 through October 2, 2026 are downloaded in `payems_source_vintages/`. The observation window and retrieval cutoff are fixed for reproducibility. Future revisions after the retrieval cutoff are outside this dataset.

- `payems_vintages.csv`: 91 initial-publication or changed-value records, with the requested columns **series name, month measured, published on, value**. A repeated unchanged value does not create a new publication event. `published on` is the ALFRED vintage date when the value first appears or changes within the captured vintage history. These dates represent ALFRED availability, without a separately verified BLS intraday timestamp.
- `payems_all_vintage_snapshots.csv`: all 336 nonmissing month–vintage combinations, including unchanged values, using the same four columns. Here `published on` identifies the snapshot's vintage date; it does not mean that every carried-forward value was newly published that day. This companion preserves every available vintage for the assignment.
- Missing or not-yet-released observations are not converted into zeros. A measured month can appear later than the month immediately following it; dates are taken from ALFRED rather than an assumed monthly release schedule.

## Rule that prevents look-ahead

For each series and measured month:

1. Keep only records with `published on <= decision date`.
2. Select the record with the latest remaining publication date.
3. Leave a month absent if it had no eligible publication. Never fill it with a future vintage.

Month measured identifies what the number describes. Published on identifies when that version becomes eligible. Selecting the latest value from today's data, or filtering only on month measured, would introduce information unavailable at the historical decision.

The default decision-date convention is end of day, including the day's vintage. `--before-release` excludes same-day vintages for a decision made before that day's release. Date-only data cannot establish exact intraday availability. A real trading timestamp requires confirmed publication times and a timezone.

## Three rows checked against ALFRED

A separate retrieval of the [November 1, 2024 ALFRED vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&cosd=2024-08-01&coed=2026-09-01&vintage_date=2024-11-01) is saved as `payems_three_row_check_source.csv`. Its three rows were compared with the corresponding rows in the all-vintage table and fixed expected values. This verifies extraction and table construction against ALFRED; it is not independent verification of BLS's underlying estimates.

| Series | Month measured | Published on / vintage | Table value | ALFRED value | Result |
|---|---|---|---:|---:|---|
| PAYEMS | 2024-08-01 | 2024-11-01 | 158770 | 158770 | PASS |
| PAYEMS | 2024-09-01 | 2024-11-01 | 158993 | 158993 | PASS |
| PAYEMS | 2024-10-01 | 2024-11-01 | 159005 | 159005 | PASS |

All values are thousands of persons. The first day represents the measured month, not the payroll release date.

## Historical proof: October 4, 2024, after release

The ALFRED September 6, October 4 and November 1 vintage files establish these versions for August 2024:

| Published on | August 2024 value | Eligible on October 4 after release? |
|---|---:|---|
| 2024-09-06 | 158779 | Yes, superseded by October 4 version |
| 2024-10-04 | 158851 | Yes, selected |
| 2024-11-01 | 158770 | No, future revision |

The resulting October 4 end-of-day output is saved in `payems_asof_2024-10-04.csv`:

| Month measured | Selected published on | Knowable value |
|---|---|---:|
| 2024-08-01 | 2024-10-04 | 158851 |
| 2024-09-01 | 2024-10-04 | 159105 |

October 2024 is absent because it had not been released. Before the October 4 release, only August is eligible within this window, at its September 6 value of 158779. Data before August 2024 are outside the exercise's coverage, so absence here does not mean no earlier history was publicly available.

## Reproduce and verification

From the course working folder:

```sh
python3 payems_verify.py
python3 payems_point_in_time.py --decision-date 2024-10-04
python3 payems_point_in_time.py --decision-date 2024-10-04 --before-release
```

`payems_download.py` retrieves source snapshots and resumes cached downloads. Building checks that every vintage date on the saved ALFRED page exists and that each CSV header matches the requested vintage. It requires at least 26 measured months before producing the tables.

Verification passed on October 27, 2026: three ALFRED row comparisons; seven expected date/boundary cases covering no release, initial release, before-release exclusion, and revisions; reversed-input order checks; rejection of conflicting duplicate publications. Expected historical values are explicit in `payems_verify.py`, rather than calculated by the filter itself.

No fund returns, forecasts or portfolio allocations were changed. Next required input: the assigned known-answer data, decision date and expected result, to establish the lab's requested known-answer match.

AI assistance: data retrieval, code, checks and draft explanation prepared with Codex for the course exercise. The student's source review and final judgments remain their own.
