"""Ordered provenance gates; instructor-authored 12-row classroom fixture.

Run: python3 provenance_gate.py
No market data or API credentials needed. Date-only cutoff is inclusive.
"""
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CUTOFF = date(2026, 3, 31)
FIXTURE = [
    (1, 'AAA', '2026-01', '2026-02-10', '101.0'),
    (2, 'AAA', '2026-02', '2026-03-10', '104.0'),
    (3, 'AAA', '2026-03', '2026-04-10', '109.0'),
    (4, 'AAA', '2026-02', '2026-03-25', '103.0'),
    (5, 'BBB', '2026-01', '2026-02-10', '98.0'),
    (6, 'BBB', '2026-02', '2026-03-10', '97.0'),
    (7, 'BBB', '2026-02', '2026-03-10', '97.0'),
    (8, 'BBB', '2026-03', '2026-04-10', '92.0'),
    (9, 'CCC', '2026-01', '2026-02-10', '110.0'),
    (10, 'CCC', '2026-02', '2026-04-05', '112.0'),
    (11, '', '2026-02', '2026-03-10', '99.0'),
    (12, 'CCC', '2026-02', '2026-03-10', '111.0'),
]

def gate(rows, cutoff):
    """Return admitted rows and an audit keyed by original source row ID.

    Row ID is excluded from exact-record duplicate comparisons. Earliest
    source occurrence is retained. Conflicting same-date publications are
    rejected because the four rules do not resolve that ambiguity.
    """
    rows = list(rows)
    ids = [r[0] for r in rows]
    if len(set(ids)) != len(ids):
        raise ValueError('Source row IDs must be unique')
    audit, active = {}, []
    for r in rows:  # Rule 1
        if not r[1].strip():
            audit[r[0]] = ('quarantined', '1: no ticker')
        else:
            active.append(r)
    seen, retained = {}, []
    for r in active:  # Rule 2
        if r[1:] in seen:
            audit[r[0]] = ('removed', f'2: exact duplicate of row {seen[r[1:]]}')
        else:
            seen[r[1:]] = r[0]
            retained.append(r)
    active = []
    for r in retained:  # Rule 3
        if date.fromisoformat(r[3]) > cutoff:
            audit[r[0]] = ('removed', '3: published after decision date')
        else:
            active.append(r)
    latest = {}
    for r in active:  # Rule 4, only after excluding future publications
        key = r[1:3]
        old = latest.get(key)
        if old and old[3] == r[3] and old[4] != r[4]:
            raise ValueError(f'Conflicting same-date publications: {old[0]}, {r[0]}')
        if old is None or r[3] > old[3]:
            latest[key] = r
    admitted = []
    for r in active:
        winner = latest[r[1:3]]
        if r[0] != winner[0]:
            audit[r[0]] = ('removed', f'4: superseded by knowable row {winner[0]}')
        else:
            audit[r[0]] = ('admitted', 'passed all four rules')
            admitted.append(r)
    return admitted, audit

def signals(admitted):
    output = []
    for ticker in sorted({r[1] for r in admitted}):
        rows = sorted((r for r in admitted if r[1] == ticker), key=lambda r: r[2])
        if len(rows) < 2:
            raise ValueError(f'{ticker}: previous month unavailable')
        previous, latest = rows[-2:]
        py, pm = map(int, previous[2].split('-'))
        ly, lm = map(int, latest[2].split('-'))
        if ly * 12 + lm - (py * 12 + pm) != 1:
            raise ValueError(f'{ticker}: previous observation is not previous calendar month')
        old, new = Decimal(previous[4]), Decimal(latest[4])
        if old == 0:
            raise ValueError(f'{ticker}: zero denominator')
        output.append((ticker, previous[0], latest[0], new / old - 1))
    return output

def main():
    admitted, audit = gate(FIXTURE, CUTOFF)
    expected_admitted = {1, 4, 5, 6, 9, 12}
    assert {r[0] for r in admitted} == expected_admitted
    expected_removed = {2: 4, 3: 3, 7: 2, 8: 3, 10: 3}
    for row, rule in expected_removed.items():
        assert audit[row][0] == 'removed' and audit[row][1].startswith(str(rule) + ':')
    assert audit[11] == ('quarantined', '1: no ticker')
    result = signals(admitted)
    expected = {'AAA': Decimal(2) / 101, 'BBB': -Decimal(1) / 98, 'CCC': Decimal(1) / 110}
    for ticker, _, _, change in result:
        assert abs(change - expected[ticker]) < Decimal('1e-25')
    # Inclusive date boundary and exclusion before publication.
    assert len(gate([FIXTURE[3]], date(2026, 3, 25))[0]) == 1
    assert len(gate([FIXTURE[3]], date(2026, 3, 24))[0]) == 0
    # Rule ordering: a future duplicate is removed by rule 2 first.
    future = [(20, 'AAA', '2026-03', '2026-04-10', '109.0'),
              (21, 'AAA', '2026-03', '2026-04-10', '109.0')]
    assert gate(future, CUTOFF)[1][21][1].startswith('2:')
    lines = ['# March 31, 2026 — known-answer provenance proof', '',
             'Source: the student-supplied 12-row classroom table and four ordered rules. Prices are planted training values.', '',
             'Decision cutoff: March 31, 2026, inclusive. Original row numbers are retained. Exact duplicates compare ticker, month, publication date and price, excluding row number.', '',
             '| Row | Ticker | Month measured | Published on | Price | Disposition | Reason |',
             '|---:|---|---|---|---:|---|---|']
    for r in FIXTURE:
        status, reason = audit[r[0]]
        lines.append('| ' + ' | '.join(map(str, (*r, status, reason))) + ' |')
    lines += ['', '**Reconciliation:** 12 source rows = 6 admitted + 5 removed + 1 quarantined. No row disappears from the audit.', '',
              '## Signal from admitted rows', '',
              'Return = February price / January price − 1. February is the latest knowable measured month for every ticker.', '',
              '| Ticker | January row | February row | Calculation | Return |',
              '|---|---:|---:|---|---:|']
    for ticker, old_id, new_id, change in result:
        by_id = {r[0]: r for r in admitted}
        lines.append(f'| {ticker} | {old_id} | {new_id} | {by_id[new_id][4]} / {by_id[old_id][4]} − 1 | {change:.6%} |')
    lines += ['', 'AAA uses row 4 (103.0), not superseded row 2 (104.0). Using row 2 would produce 2.970297% rather than 1.980198%. The revision reduced the knowable return by 0.990099 percentage points before the decision date.', '',
              'Rows 3 and 8 describe March but were published April 10. Row 10 describes February but was published April 5. All three came later and must be excluded. A measured month alone does not establish availability.', '',
              '## V — financial validity, separate from provenance', '',
              'Yield = 100 / price − 1 under the supplied one-year zero-coupon interpretation.', '',
              '| Ticker | January yield | February yield |',
              '|---|---:|---:|']
    for ticker, old_id, new_id, _ in result:
        old, new = Decimal(by_id[old_id][4]), Decimal(by_id[new_id][4])
        lines.append(f'| {ticker} | {Decimal(100)/old-1:.6%} | {Decimal(100)/new-1:.6%} |')
    lines += ['', 'Under the exercise’s stated financial checks, AAA and CCC prices above 100 are flagged: their implied yields are negative. The credit-price ordering fails in both months: CCC is priced above AAA and BBB, although the exercise requires AAA > BBB > CCC at equal maturity. These rows pass provenance but fail V. The four provenance rules do not authorize removing them for financial invalidity.', '',
              'The reported price returns are the assigned signal calculation, not a claim that these planted prices support a valid investment decision.', '',
              'Verification: all 12 row dispositions and all three returns matched explicitly specified expected results; publication-date equality and ordered duplicate handling also passed. Run `python3 provenance_gate.py` from this folder to reproduce.', '',
              'This completes the supplied classroom known-answer fixture. PAYEMS is the separate ALFRED application; the bond fixture is not ALFRED market data.']
    destination = ROOT / 'Lab15_known_answer_provenance_2026_03_31.md'
    destination.write_text('\n'.join(lines) + '\n')
    print('PASS: 12 dispositions, 3 returns, inclusive cutoff and gate-order checks')
    print(destination)
    for r in result:
        print(r[0], f'{r[3]:.6%}')

if __name__ == '__main__':
    main()
