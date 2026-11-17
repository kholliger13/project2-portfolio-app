"""PAYEMS publication-event table and date-based point-in-time selection.

Date-only decisions mean end of day. For a decision before that day's release,
use --before-release to exclude same-day vintages. No release time is inferred.
"""
import argparse
import csv
import re
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ['series name', 'month measured', 'published on', 'value']
NAME = 'All Employees, Total Nonfarm (PAYEMS)'

def read_rows(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))

def write_rows(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def point_in_time(rows, decision_date, before_release=False):
    cutoff = date.fromisoformat(decision_date)
    latest, seen = {}, {}
    for row in rows:
        month = date.fromisoformat(row['month measured'])
        published = date.fromisoformat(row['published on'])
        value = Decimal(row['value'])
        if not value.is_finite():
            raise ValueError('Nonfinite value')
        key = (row['series name'], month, published)
        if key in seen and seen[key] != value:
            raise ValueError(f'Conflicting publication: {key}')
        seen[key] = value
        if month > cutoff or published > cutoff or (before_release and published == cutoff):
            continue
        group = key[:2]
        if group not in latest or published > date.fromisoformat(latest[group]['published on']):
            latest[group] = row
    return [latest[key] for key in sorted(latest)]

def build():
    events, snapshots, previous = [], [], {}
    dates = sorted(set(re.findall(r'<option value="(\d{4}-\d{2}-\d{2})"',
                                 (ROOT / 'alfred_download_page.html').read_text())))
    dates = [d for d in dates if '2024-09-01' <= d <= '2026-10-27']
    paths = [ROOT / 'payems_source_vintages' / f'PAYEMS_{d}.csv' for d in dates]
    missing = [p.name for p in paths if not p.exists()]
    if missing:
        raise ValueError(f'Missing source vintages: {missing}')
    for path in paths:
        vintage = path.stem.removeprefix('PAYEMS_')
        source_rows = read_rows(path)
        if not source_rows or list(source_rows[0]) != ['observation_date', 'PAYEMS_' + vintage.replace('-', '')]:
            raise ValueError(f'Wrong vintage header: {path}')
        for source in source_rows:
            month, value = list(source.values())
            if not '2024-08-01' <= month <= '2026-09-01':
                continue
            if value in ('', '.'):
                continue
            row = dict(zip(FIELDS, [NAME, month, vintage, value]))
            snapshots.append(row)
            if previous.get(month) != Decimal(value):
                events.append(row)
                previous[month] = Decimal(value)
    if len(previous) < 26:
        raise ValueError(f'Only {len(previous)} measured months downloaded; need 26')
    write_rows(ROOT / 'payems_vintages.csv', events)
    write_rows(ROOT / 'payems_all_vintage_snapshots.csv', snapshots)
    print(f'{len(previous)} months; {len(events)} publication events; {len(snapshots)} snapshot rows')
    return events

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decision-date', help='YYYY-MM-DD; end of day unless --before-release')
    parser.add_argument('--before-release', action='store_true')
    args = parser.parse_args()
    rows = build()
    if args.decision_date:
        selected = point_in_time(rows, args.decision_date, args.before_release)
        suffix = '_before_release' if args.before_release else ''
        path = ROOT / f'payems_asof_{args.decision_date}{suffix}.csv'
        write_rows(path, selected)
        print(f'{len(selected)} knowable months -> {path.name}')

if __name__ == '__main__':
    main()
