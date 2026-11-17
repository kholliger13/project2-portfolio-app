"""Run with --live for one current and one historical request per class series."""
import argparse
from datetime import date
from io import BytesIO
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest
from asof_app import SERIES, comparison, download_asof, download_today, parse_csv


def verify():
    current = parse_csv('observation_date,DGS10\n2024-01-01,4\n2024-01-02,.\n2024-01-03,5\n2024-01-04,6\n', 'DGS10')
    historical = parse_csv('observation_date,DGS10_20240103\n2024-01-01,3\n2024-01-02,2\n2024-01-03,5\n', 'DGS10', date(2024, 1, 3))
    result = comparison('DGS10', current, historical)
    assert pd.isna(current.loc['2024-01-02', 'Value'])
    assert result['Newer values today'] == 1
    assert result['Revised values on shared dates'] == 1
    assert result['Value · as known then'] == 5
    assert result['Value · today'] == 6
    assert comparison('DGS10', current, historical.iloc[:0])['Newer values today'] is None
    earlier = parse_csv('observation_date,PAYEMS_20261028\n2026-09-01,159044\n', 'PAYEMS', date(2026, 10, 29))
    assert earlier.attrs['returned_vintage'] == date(2026, 10, 28)
    try:
        parse_csv('observation_date,PAYEMS_20261030\n2026-09-01,159044\n', 'PAYEMS', date(2026, 10, 29))
    except ValueError:
        pass
    else:
        raise AssertionError('Future vintage accepted')
    download_today.clear()
    download_asof.clear()
    def response(url, timeout):
        from urllib.parse import parse_qs, urlparse
        params = parse_qs(urlparse(url).query)
        series = params['id'][0]
        if series == 'UNKNOWN_TEST':
            raise ValueError('Unknown series')
        suffix = '_' + params['vintage_date'][0].replace('-', '') if 'vintage_date' in params else ''
        return BytesIO(f'observation_date,{series}{suffix}\n2024-01-01,4\n2024-01-02,.\n2024-01-03,5\n'.encode())
    with patch('asof_app.urlopen', side_effect=response) as mock, patch('urllib.request.urlopen', side_effect=response):
        for _ in range(2):
            download_today('DGS10', date.today())
            download_asof('DGS10', date(2024, 1, 3), date.today())
        assert mock.call_count == 2, 'Cache should avoid duplicate requests'
        urls = [call.args[0] for call in mock.call_args_list]
        assert urls == ['https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10',
                        'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2024-01-03']
        app = AppTest.from_file('asof_app.py').run(timeout=30)
        assert not app.exception and not app.error
        assert app.multiselect[0].value == list(SERIES)
        assert app.date_input[0].value == date(2020, 1, 1)
        assert app.date_input[1].value == date.today()
        assert app.text_input[0].value == 'PAYEMS'
        assert len(app.dataframe[0].value) == 5
        app.text_input[0].set_value('UNKNOWN_TEST').run(timeout=30)
        assert not app.exception and len(app.error) == 1
        assert len(app.dataframe[0].value) == 5
        app.text_input[0].set_value('PAYEMS').run(timeout=30)
        assert not app.exception and not app.error
        assert len(app.dataframe[0].value) == 5
        app.multiselect[0].set_value([]).run(timeout=30)
        app.text_input[0].set_value('').run(timeout=30)
        assert not app.exception
    download_today.clear()
    download_asof.clear()
    print('PASS: missing days, newer and revised counts, empty vintage, exact URLs, caching, default controls, unknown-ID isolation, custom ID, empty selection.')


def live():
    for series in SERIES:
        current = download_today(series, date.today())
        historical = download_asof(series, date(2024, 10, 4), date.today())
        assert not current.empty and not historical.empty
        assert historical.index.max() <= pd.Timestamp('2024-10-04')
        row = comparison(series, current, historical)
        print(series, 'then:', row['Last measured date · as known then'], row['Value · as known then'],
              'today:', row['Last measured date · today'], row['Value · today'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    if args.live:
        live()
    else:
        verify()
