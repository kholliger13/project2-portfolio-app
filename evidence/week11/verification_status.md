# Lab verification — completed

Public SEC EDGAR companyfacts downloaded on 2026-11-03 using Kayla Holliger's contact User-Agent. No FAskills installation or paid data sources used. Original downloaded facts are preserved in reports.

- COST: every fiscal-year date and monetary value matches the supplied FY2022–FY2026 benchmark. ROE matches at the benchmark's one-decimal precision. All three checks pass. Owner earnings and net income both end above their starting levels.
- JPM: capital spending and owner earnings are `not found` in all five years. Both owner-earnings checks are `not known`. The saved memo explicitly says it cannot judge owner earnings. The ROE check fails.
- Both model-authored memos are saved as Markdown, contain only numbers from their script output, and are bound to their reports by a hash.
- Streamlit app tests against the downloaded reports verify COST's chart, table, memo, and **My decision:** line. Editing the memo to add `40.0%` triggers the unsupported-number error. The edit is temporary and does not corrupt the saved memo.
- Streamlit app tests also verify JPM's missing values, unknown checks, and memo limitation.
- Five calculation regression tests pass. Skill-format validation passed at creation.

Commands from this folder, using `../.venv/bin/python`: `verify_cost.py`, `verify_jpm.py`, `test_live_app.py`, and `test_lab.py`.

The number checker checks numeric presence, not semantic correctness. The memos' numeric claims were also reviewed against the printed table. These financial checks support a business-quality judgment but cannot by themselves establish a durable moat or management quality.
