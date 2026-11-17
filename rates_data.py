"""ALFRED date-only snapshots. Run from the course folder; no API key needed."""
import csv
import hashlib
import io
import json
import math
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'rates_source_vintages'
SERIES = {
    'BAA': "Moody's seasoned Baa corporate bond yield",
    'FEDFUNDS': 'Effective federal funds rate (monthly)',
    'DGS10': '10-year Treasury yield',
    'MORTGAGE30US': '30-year fixed mortgage rate',
    'DGS2': '2-year Treasury yield',
    'DFF': 'Effective federal funds rate (daily)',
}
CLASS_SERIES = ['BAA', 'FEDFUNDS', 'DGS10', 'MORTGAGE30US']
FREQUENCY = {'BAA': 'Monthly', 'FEDFUNDS': 'Monthly', 'DGS10': 'Daily',
             'MORTGAGE30US': 'Weekly, ending Thursday', 'DGS2': 'Daily', 'DFF': 'Daily'}

def request_details(series, start, decision, before=False):
    if series not in SERIES:
        raise ValueError('Unsupported rate series')
    start, decision = date.fromisoformat(str(start)), date.fromisoformat(str(decision))
    if start > decision:
        raise ValueError('Observation start must be on or before the decision date')
    if decision > date.today():
        raise ValueError('Future decision dates cannot be verified')
    vintage = decision - timedelta(days=1) if before else decision
    query = urlencode(dict(id=series, cosd=start.isoformat(), coed=decision.isoformat(),
                           vintage_date=vintage.isoformat()))
    return vintage, 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?' + query

def parse_snapshot(content, series, vintage, start, decision):
    """Reject HTML, wrong vintages, nonfinite values and duplicate dates."""
    reader = csv.DictReader(io.StringIO(content))
    expected = ['observation_date', f'{series}_{vintage:%Y%m%d}']
    if reader.fieldnames != expected:
        raise ValueError(f'ALFRED response does not match requested vintage: {reader.fieldnames}')
    rows, seen = [], set()
    for row in reader:
        observed = date.fromisoformat(row['observation_date'])
        if observed in seen:
            raise ValueError('Duplicate observation date in source')
        seen.add(observed)
        if not date.fromisoformat(str(start)) <= observed <= date.fromisoformat(str(decision)):
            continue
        raw = row[expected[1]]
        value = None if raw in ('', '.') else float(raw)
        if value is not None and not math.isfinite(value):
            raise ValueError('Nonfinite rate')
        rows.append({'observation date': observed.isoformat(), 'value': value})
    return sorted(rows, key=lambda r: r['observation date'])

def snapshot(series, start, decision, before=False, refresh=False):
    vintage, url = request_details(series, start, decision, before)
    CACHE.mkdir(exist_ok=True)
    stem = f'{series}_{start}_{decision}_{vintage}'
    path, meta_path = CACHE / (stem + '.csv'), CACHE / (stem + '.json')
    if not refresh and path.exists() and meta_path.exists():
        content = path.read_text()
        meta = json.loads(meta_path.read_text())
        if meta['source_url'] != url or meta['sha256'] != hashlib.sha256(content.encode()).hexdigest():
            raise ValueError('Cached source integrity check failed')
    else:
        with urlopen(url, timeout=35) as response:
            content = response.read().decode('utf-8-sig')
        parse_snapshot(content, series, vintage, start, decision)
        meta = {'source_url': url, 'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
                'series': series, 'requested_vintage': vintage.isoformat(),
                'sha256': hashlib.sha256(content.encode()).hexdigest()}
        path.write_text(content)
        meta_path.write_text(json.dumps(meta, indent=2))
    rows = parse_snapshot(content, series, vintage, start, decision)
    return rows, meta
