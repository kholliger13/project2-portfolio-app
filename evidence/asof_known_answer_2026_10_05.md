# Live known-answer proof — October 5, 2026

Executed asof_app.py through Streamlit AppTest with As known on set to 2026-10-05.
Downloads use the app’s real public FRED/ALFRED CSV functions; no mocked data or substituted values.
Checked on: 2026-10-29. Expected results were supplied by the student.

| Series | Expected measured date | Actual measured date | Expected value | Actual value | Result |
|---|---|---|---:|---:|---|
| BAA | 2026-09-01 | 2026-09-01 | 6.47 | 6.47 | PASS |
| FEDFUNDS | 2026-09-01 | 2026-09-01 | 3.75 | 3.75 | PASS |
| DGS10 | 2026-10-02 | 2026-10-02 | 5.28 | 5.28 | PASS |
| MORTGAGE30US | 2026-10-01 | 2026-10-01 | 7.28 | 7.28 | PASS |

Monthly series use the first day as the label for the measured month; September 1 means September 2026, not a September 1 publication.

## Historical source requests

- [BAA vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-05)
- [FEDFUNDS vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=FEDFUNDS&vintage_date=2026-10-05)
- [DGS10 vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-05)
- [MORTGAGE30US vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=MORTGAGE30US&vintage_date=2026-10-05)
