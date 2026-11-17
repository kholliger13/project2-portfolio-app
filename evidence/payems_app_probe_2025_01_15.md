# PAYEMS live app probe — January 15, 2025

Executed on 2026-10-29 using the actual Streamlit page, custom ID PAYEMS, and As known on 2025-01-15.
Both CSV responses came from live public endpoints; the wrapper only recorded bytes and did not substitute data.

- Latest measured date known then: 2024-12-01
- Value known then: 159,536 thousand persons
- Today’s value for that same December 2024 observation: 158,316 thousand persons
- Revision to December 2024: -1,220 thousand persons
- Revised values across shared nonmissing dates: 381 of 1,032
- Newer values today: 21

| Check | Result |
|---|---|
| Latest known measured month is December 2024 | PASS |
| Known value is 159,536 | PASS |
| Today’s December 2024 value is lower | PASS |
| Revised count is greater than zero | PASS |

The table’s “Value · today” is the latest current observation, not the current December 2024 observation. The same-month comparison above reads December 2024 explicitly.

The revised count covers the full downloaded history, not just observations after the chart’s start date.

## Source requests

- [today](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS)
- [asof](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2025-01-15)
