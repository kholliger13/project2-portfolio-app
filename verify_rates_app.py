"""Boundary, source-integrity and UI checks for the rates app."""
from datetime import date
from rates_data import CLASS_SERIES, FREQUENCY, parse_snapshot, request_details, snapshot
from payems_point_in_time import ROOT, point_in_time, read_rows

def displayed_payems(app):
    panel = next(frame.value for frame in app.dataframe
                 if {'month measured', 'value'} <= set(frame.value.columns)
                 and 'eligible by cutoff' not in frame.value.columns)
    return panel.set_index('month measured')['value'].to_dict()


def verify():
    vintage, _ = request_details('DGS10', '2024-08-01', '2024-10-04', True)
    assert vintage == date(2024, 10, 3)
    source = 'observation_date,DGS10_20241004\n2024-10-03,3.85\n2024-10-04,.\n'
    rows = parse_snapshot(source, 'DGS10', date(2024, 10, 4), '2024-08-01', '2024-10-04')
    assert rows == [{'observation date': '2024-10-03', 'value': 3.85},
                    {'observation date': '2024-10-04', 'value': None}]
    for invalid in [source.replace('20241004', '20241005'), source.replace('3.85', 'NaN'),
                    source + '2024-10-03,3.86\n', '<html>blocked</html>']:
        try:
            parse_snapshot(invalid, 'DGS10', date(2024, 10, 4), '2024-08-01', '2024-10-04')
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid source accepted')
    rows, meta = snapshot('DGS10', '2024-08-01', '2024-10-04')
    available = [r for r in rows if r['value'] is not None]
    assert available[-1] == {'observation date': '2024-10-03', 'value': 3.85}
    assert meta['requested_vintage'] == '2024-10-04'
    assert CLASS_SERIES == ['BAA', 'FEDFUNDS', 'DGS10', 'MORTGAGE30US']
    assert FREQUENCY['FEDFUNDS'] == 'Monthly' and FREQUENCY['MORTGAGE30US'].startswith('Weekly')
    for series in CLASS_SERIES:
        rows, meta = snapshot(series, '2024-08-01', '2024-10-04')
        assert rows and meta['series'] == series
        assert all(r['observation date'] <= '2024-10-04' for r in rows)
    events = read_rows(ROOT / 'payems_vintages.csv')
    assert {r['month measured']: r['value'] for r in point_in_time(events, '2024-10-04')} == {
        '2024-08-01': '158851', '2024-09-01': '159105'}
    assert {r['month measured']: r['value'] for r in point_in_time(events, '2024-10-04', True)} == {
        '2024-08-01': '158779'}
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(ROOT / 'rates_app.py')).run(timeout=120)
    assert not app.exception, app.exception
    assert not app.error, [e.value for e in app.error]
    assert app.multiselect[0].value == CLASS_SERIES
    assert len(app.metric) == 4
    assert app.checkbox[0].value
    assert displayed_payems(app) == {'2024-08-01': 158779}
    assert any("signal unavailable" in entry.value for entry in app.info)
    app.checkbox[0].uncheck().run(timeout=120)
    assert not app.exception and not app.error
    assert displayed_payems(app) == {'2024-08-01': 158851, '2024-09-01': 159105}
    assert any("same-day comparison for 2024-09: +254 thousand jobs" in entry.value
               for entry in app.markdown)
    assert not any("Project 2 PAYEMS monitoring signal for" in entry.value for entry in app.markdown)
    app.multiselect[0].set_value([]).run(timeout=120)
    app.checkbox[0].check().run(timeout=120)
    app.date_input[0].set_value(date(2024, 10, 5)).run(timeout=120)
    assert not app.exception
    assert any("Project 2 PAYEMS monitoring signal for 2024-09: +254 thousand jobs" in entry.value
               for entry in app.markdown)
    assert not any("Committee review triggered" in entry.value for entry in app.warning)
    app.date_input[0].set_value(date(2026, 3, 7)).run(timeout=120)
    assert not app.exception
    assert any("monitoring signal for 2026-02: -92 thousand jobs" in entry.value
               for entry in app.markdown)
    assert any("Committee review triggered" in entry.value for entry in app.warning)
    app.date_input[0].set_value(date(2026, 10, 3)).run(timeout=120)
    assert not app.exception
    assert any("monitoring signal for 2026-09: +29 thousand jobs" in entry.value
               for entry in app.markdown)
    assert not any("Committee review triggered" in entry.value for entry in app.warning)
    app.date_input[0].set_value(date(2024, 7, 1)).run(timeout=120)
    assert not app.exception
    assert app.date_input[1].value <= date(2024, 7, 1)
    print('PASS: previous-day cutoff; missing values; wrong vintage, HTML, duplicate and nonfinite rejection; historical DGS10 source value; PAYEMS release boundary; Streamlit default, before-release and empty selection.')

if __name__ == '__main__':
    verify()
