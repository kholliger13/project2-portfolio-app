"""Source spot checks and independently specified historical boundary answers."""
from payems_point_in_time import ROOT, FIELDS, NAME, build, point_in_time, read_rows, write_rows

def verify():
    events = build()
    # Values read from a separately retrieved ALFRED 2024-11-01 CSV.
    expected = {'2024-08-01': '158770', '2024-09-01': '158993', '2024-10-01': '159005'}
    source = read_rows(ROOT / 'payems_three_row_check_source.csv')
    source_values = {r['observation_date']: r['PAYEMS_20241101'] for r in source}
    snapshot = {r['month measured']: r['value'] for r in read_rows(ROOT / 'payems_all_vintage_snapshots.csv')
                if r['published on'] == '2024-11-01'}
    for month, value in expected.items():
        assert source_values[month] == value == snapshot[month], (month, value)
    # Expected answers explicitly fixed from the earlier ALFRED source snapshots.
    cases = [
        ('2024-09-05', False, {}),
        ('2024-09-06', True, {}),
        ('2024-09-06', False, {'2024-08-01': '158779'}),
        ('2024-10-03', False, {'2024-08-01': '158779'}),
        ('2024-10-04', True, {'2024-08-01': '158779'}),
        ('2024-10-04', False, {'2024-08-01': '158851', '2024-09-01': '159105'}),
        ('2024-11-01', False, expected),
    ]
    for decision, before, answer in cases:
        result = point_in_time(events, decision, before)
        assert {r['month measured']: r['value'] for r in result} == answer, (decision, before, result)
        assert point_in_time(list(reversed(events)), decision, before) == result
    conflict = [dict(zip(FIELDS, [NAME, '2024-08-01', '2024-09-06', v])) for v in ['1', '2']]
    try:
        point_in_time(conflict, '2024-09-06')
    except ValueError:
        pass
    else:
        raise AssertionError('Conflicting duplicate accepted')
    write_rows(ROOT / 'payems_asof_2024-10-04.csv', point_in_time(events, '2024-10-04'))
    print('PASS: 3 ALFRED row checks, 7 date/boundary cases, shuffled-input checks, conflicting duplicate rejection')
    print('Instructor decision date / known answer: pending; historical source-based examples are not the instructor key.')

if __name__ == '__main__':
    verify()
