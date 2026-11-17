"""Compare asof.py against the student-supplied instructor answer key."""
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
from pathlib import Path
import asof


def main():
    decision = date.fromisoformat(asof.DECISION_DATE)
    assert decision == date(2026, 3, 31), 'Known-answer cutoff changed'
    source = asof.parse_table(asof.RAW_TABLE)
    assert len(source) == 12
    current = source
    expected_removed = [[11], [7], [3, 8, 10], [2]]
    expected_remaining = [11, 10, 7, 6]
    report = ['KNOWN-ANSWER COMPARISON: asof.py', 'Decision date: 2026-03-31', '']
    for (name, rule), expected, count in zip(asof.RULES, expected_removed, expected_remaining):
        current, removed = rule(current, decision)
        actual = [r['row'] for r in removed]
        assert actual == expected, (name, actual, expected)
        assert len(current) == count
        report.append(f'PASS {name}: rows {actual}; {count} remain')
    ids = [r['row'] for r in current]
    assert ids == [1, 4, 5, 6, 9, 12], ids
    report.append(f'PASS as-of panel: {ids}')
    actual_panel = [(r['row'], r['ticker'], r['month'], r['published'].isoformat(), r['price']) for r in current]
    assert actual_panel == [
        (1, 'AAA', '2026-01', '2026-02-10', 101.0),
        (4, 'AAA', '2026-02', '2026-03-25', 103.0),
        (5, 'BBB', '2026-01', '2026-02-10', 98.0),
        (6, 'BBB', '2026-02', '2026-03-10', 97.0),
        (9, 'CCC', '2026-01', '2026-02-10', 110.0),
        (12, 'CCC', '2026-02', '2026-03-10', 111.0),
    ]
    naive, _ = asof.keep_latest_publication([r for r in source if r['ticker']])
    expected_asof = {'AAA': ('2026-02', '+1.98'), 'BBB': ('2026-02', '-1.02'), 'CCC': ('2026-02', '+0.91')}
    expected_naive = {'AAA': ('2026-03', '+5.83'), 'BBB': ('2026-03', '-5.15'), 'CCC': ('2026-02', '+1.82')}
    for label, rows, expected in [('AS-OF', current, expected_asof), ('NAIVE', naive, expected_naive)]:
        result = asof.signals(rows)
        assert set(result) == set(expected)
        for ticker, (month, pct) in expected.items():
            actual = result[ticker]
            assert (actual[0], f'{actual[4]:+.2f}') == (month, pct), (label, ticker, actual)
            assert actual[1] == asof.prev_month(month)
            report.append(f'PASS {label} {ticker}: {actual[4]:+.2f}% ({actual[0]})')
    aaa_feb = next(r for r in current if r['ticker'] == 'AAA' and r['month'] == '2026-02')
    assert aaa_feb['row'] == 4 and aaa_feb['price'] == 103.0
    assert f'{asof.signals(current)["AAA"][4]:+.2f}' != '+2.97'
    ccc_naive = next(r for r in naive if r['ticker'] == 'CCC' and r['month'] == '2026-02')
    assert ccc_naive['row'] == 10 and ccc_naive['price'] == 112.0
    report += ['PASS revision checks: AAA uses row 4 (103.0); naive CCC uses row 10 (112.0)',
               '', 'ALL KNOWN-ANSWER VALUES MATCH. No code fixes required.',
               'Signal comparisons use the answer key precision: two decimal percentage points.']
    captured = StringIO()
    with redirect_stdout(captured):
        asof.main()
    (Path(__file__).parent / 'asof_known_answer_proof.txt').write_text(
        '\n'.join(report) + '\n\nACTUAL PROGRAM OUTPUT\n' + captured.getvalue())
    print('\n'.join(report))


if __name__ == '__main__':
    main()
