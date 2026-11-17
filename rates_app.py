"""Run: .venv/bin/python -m streamlit run rates_app.py"""
from datetime import date
import json
import pandas as pd
import streamlit as st
from rates_data import ROOT, SERIES, CLASS_SERIES, FREQUENCY, snapshot
from payems_point_in_time import point_in_time, read_rows

st.set_page_config(page_title='Rates · As Known', page_icon='📈', layout='wide')
st.markdown('''<style>
.stApp {background:#f6f8fb} h1,h2,h3 {color:#173e61}
[data-testid="stSidebar"] {background:#eaf0f6}
[data-testid="stMetric"] {background:white;padding:18px;border-top:3px solid #2879ad;border-radius:5px}
</style>''', unsafe_allow_html=True)
st.caption('AI FINANCE 2026 / KAYLA HOLLIGER')
st.title('Rates · As Known')
st.write('Explore the economic information available on a historical date.')
st.sidebar.header('Choose your information set')
decision = st.sidebar.date_input('Decision date', date(2024, 10, 4), max_value=date.today())
before = st.sidebar.checkbox('Exclude all same-day publications', value=False,
                            help='Uses the previous calendar day’s vintage. This is a conservative date-only convention, not an intraday reconstruction.')
if st.session_state.get('rates_start', decision) > decision:
    del st.session_state['rates_start']
start = st.sidebar.date_input('Observation window starts', min(date(2024, 8, 1), decision),
                              max_value=decision, key='rates_start')
selected = st.sidebar.multiselect('Rates', list(SERIES), default=CLASS_SERIES,
                                  format_func=lambda s: f'{s} · {SERIES[s]} · {FREQUENCY[s]}')
refresh = st.sidebar.button('Refresh selected vintages from ALFRED')
st.sidebar.caption('Rates: percent per year, not bond prices or total returns. ALFRED archive availability is date-based.')
st.sidebar.caption('To view the latest available data, select today and refresh. Saved retrieval times appear with each source.')
rates_tab, payroll_tab, eligibility_tab = st.tabs(['Rates explorer', '10/27 series · PAYEMS', 'Project 2 review'])

with rates_tab:
    st.subheader(f'Information set: {decision:%B %d, %Y}')
    st.caption('Previous-day vintage' if before else 'End-of-day vintage, including same-day archive updates')
    st.info('Observation date labels the measured day, week, or month; it is not the publication date. The requested vintage selects the historical information set. A snapshot does not identify each observation’s first publication date.')
    frames, evidence = [], []
    columns = st.columns(max(1, len(selected)))
    for col, series in zip(columns, selected):
        try:
            rows, meta = snapshot(series, str(start), str(decision), before, refresh=refresh)
            evidence.append(meta)
            frame = pd.DataFrame(rows, columns=['observation date', 'value'])
            available = frame.dropna(subset=['value'])
            with col:
                st.metric(SERIES[series], 'Unavailable' if available.empty else f"{available.iloc[-1]['value']:.2f}%")
                if not available.empty:
                    st.caption(f"Latest observation: {available.iloc[-1]['observation date']}")
                st.caption(FREQUENCY[series])
            if not frame.empty:
                frame['series'] = series
                frame['frequency'] = FREQUENCY[series]
                frame['requested vintage'] = meta['requested_vintage']
                frames.append(frame)
            with st.expander(f'{series} · source and vintage'):
                st.write(f"Requested ALFRED vintage: {meta['requested_vintage']}")
                st.write(f"Retrieved (UTC): {meta['retrieved_at_utc']}")
                st.link_button('Open original ALFRED CSV', meta['source_url'])
                st.link_button('FRED series definition', f'https://fred.stlouisfed.org/series/{series}')
                st.caption('Source bytes are cached locally with a SHA-256 integrity hash. Missing observations stay missing.')
        except Exception as exc:
            with col:
                st.error(f'{series}: source unavailable. {exc}')
    if frames:
        panel = pd.concat(frames, ignore_index=True)
        chart = panel.pivot(index='observation date', columns='series', values='value')
        chart.index = pd.to_datetime(chart.index)
        for frequency in dict.fromkeys(FREQUENCY[s] for s in selected if s in chart.columns):
            ids = [s for s in selected if s in chart.columns and FREQUENCY[s] == frequency]
            st.markdown(f'**{frequency} observations**')
            group = panel[panel['series'].isin(ids)].pivot(index='observation date', columns='series', values='value')
            group.index = pd.to_datetime(group.index)
            st.line_chart(group, y_label='Annual rate (%)', x_label='Observation period', height=230)
        st.caption('Series retain their native frequencies. No daily filling or interpolation is applied to monthly or weekly rates. Monthly date labels represent the measured month, not when its full-month average became available.')
        if {'DGS2', 'DGS10'} <= set(chart.columns):
            spread = (chart['DGS10'] - chart['DGS2']).dropna()
            if not spread.empty:
                st.metric('10-year minus 2-year Treasury spread', f'{spread.iloc[-1]:+.2f} percentage points')
                st.caption(f'Latest common nonmissing observation: {spread.index[-1]:%Y-%m-%d}')
        st.dataframe(panel, hide_index=True, width='stretch')
        st.download_button('Download selected vintage data', panel.to_csv(index=False),
                           f'rates_asof_{decision}.csv', 'text/csv')
        st.download_button('Download source manifest', json.dumps(evidence, indent=2),
                           f'rates_sources_{decision}.json', 'application/json')
    elif not selected:
        st.info('Choose at least one rate to explore.')

with payroll_tab:
    st.subheader('PAYEMS · employment levels, not interest rates')
    st.caption('Monthly · seasonally adjusted · thousands of persons. Saved October 27, 2026.')
    st.link_button('PAYEMS · your prework series on FRED', 'https://fred.stlouisfed.org/series/PAYEMS')
    events = read_rows(ROOT / 'payems_vintages.csv')
    eligible = point_in_time(events, str(decision), before)
    eligible = [r for r in eligible if str(start) <= r['month measured'] <= str(decision)]
    st.write('For each measured month, keep the latest publication eligible by the cutoff. Later revisions remain excluded.')
    if decision > date(2026, 10, 27):
        st.warning('This frozen dataset stops at the October 27 retrieval cutoff. It cannot establish what became available after that date.')
    if eligible:
        panel = pd.DataFrame(eligible)
        panel['value'] = pd.to_numeric(panel['value'])
        st.line_chart(panel.set_index('month measured')['value'], y_label='Thousands of persons')
        st.dataframe(panel, hide_index=True, width='stretch')
        st.download_button('Download knowable PAYEMS panel', panel.to_csv(index=False), f'payems_selected_{decision}.csv', 'text/csv')
    else:
        st.info('No eligible records in this observation window. The saved history begins with August 2024, first available September 6, 2024.')
    with st.expander('Inspect every captured version, including future revisions'):
        audit = pd.DataFrame(events)
        audit['eligible by cutoff'] = audit['published on'].map(lambda d: d < str(decision) if before else d <= str(decision))
        st.dataframe(audit, hide_index=True, width='stretch')
    st.caption('Coverage: August 2024–September 2026; 25 captured vintages. No verified intraday release timestamps. Dates reflect captured ALFRED availability.')

with eligibility_tab:
    st.subheader('Project 2 · provisional decision')
    st.warning('HOLD for final Project 2 admission: the assignment rules and required decision dates have not been provided.')
    st.markdown('''PAYEMS is a candidate economic input. Its saved vintages support a date-based historical analysis within the captured coverage. It is an employment series, so it does not satisfy a requirement for an interest-rate series.

The 10/27 checks support extraction and historical cutoff logic. The classroom AAA/BBB/CCC known-answer exercise tests the filtering method separately; it does not certify PAYEMS against a Project 2 answer key.

Before final admission, match Project 2’s required series, sample length, decision timing, transformations, and verification requirements. Any predictor must be formed entirely from the information set available at each decision. Predictive usefulness remains untested.''')
    st.dataframe(pd.DataFrame([
        ['Source and revision history', 'Supported', 'Archived ALFRED snapshots and event table'],
        ['Historical cutoff checks', 'Supported', 'Seven boundary cases and three source-row comparisons'],
        ['Interest-rate series requirement', 'Fails if required', 'PAYEMS measures employment'],
        ['Intraday decisions', 'Unverified', 'Date-only vintages; no release timestamp verification'],
        ['Required sample and series', 'Pending', 'Need Project 2 instructions'],
        ['Predictive value', 'Untested', 'Economic rationale alone does not establish a useful signal'],
    ], columns=['Review', 'Status', 'Evidence / limitation']), hide_index=True, width='stretch')
st.caption('Independent course app inspired by FRED; not affiliated with the Federal Reserve. AI assistance: Codex helped build the app and checks.')
