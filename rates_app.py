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
before = st.sidebar.checkbox('Exclude all same-day publications', value=True,
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

def payroll_change(rows):
    if len(rows) < 2:
        return None
    previous, latest = rows[-2:]
    month = pd.Period(latest['month measured'], freq='M')
    if pd.Period(previous['month measured'], freq='M') + 1 != month:
        return None
    return month, float(latest['value']) - float(previous['value'])


with payroll_tab:
    st.subheader('PAYEMS · employment levels, not interest rates')
    st.caption('Monthly · seasonally adjusted · thousands of persons. Saved October 27, 2026.')
    st.link_button('PAYEMS · your prework series on FRED', 'https://fred.stlouisfed.org/series/PAYEMS')
    events = read_rows(ROOT / 'payems_vintages.csv')
    eligible = point_in_time(events, str(decision), before)
    outside_capture = decision > date(2026, 10, 27)
    signal = payroll_change(eligible)
    if outside_capture:
        st.warning("Project 2 monitoring signal unavailable outside the captured decision dates.")
    elif signal is None:
        st.info("PAYEMS monthly change signal unavailable: two consecutive months are required.")
    else:
        month, change = signal
        label = "Project 2 PAYEMS monitoring signal" if before else "PAYEMS same-day comparison"
        st.write(f"{label} for {month}: {change:+,g} thousand jobs.")
        if before and change < 0:
            prior_month = (pd.Timestamp(decision) - pd.DateOffset(months=1)).date()
            previous_decision = st.date_input(
                "Previous month's committee decision date", value=None,
                min_value=prior_month.replace(day=1),
                max_value=decision.replace(day=1) - pd.Timedelta(days=1),
                key=f"prior_payems_decision_{decision}",
            )
            prior_signal = None
            if previous_decision is not None:
                prior_signal = payroll_change(point_in_time(events, str(previous_decision), True))
            if prior_signal is None or prior_signal[0] + 1 != month:
                st.info("Review trigger unavailable until both decision dates have consecutive payroll readings.")
            else:
                prior_period, prior_change = prior_signal
                st.caption(f"Prior decision {previous_decision}: {prior_period} payroll change "
                           f"{prior_change:+,g} thousand jobs.")
                if prior_change < 0:
                    st.warning("Committee review triggered: two consecutive negative PAYEMS readings.")
    if not before:
        st.caption("Same-day values are shown for comparison only. Project 2 uses the previous-day vintage.")
    visible = [r for r in eligible if str(start) <= r['month measured']]
    if visible:
        panel = pd.DataFrame(visible)
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
    st.subheader('Project 2 · PAYEMS admitted for monitoring')
    st.markdown('''Use the previous calendar day's ALFRED information set. Subtract the prior month's
eligible payroll level from the latest month's eligible level. Refer the pilot to the committee if the point-in-time PAYEMS change is negative for two consecutive months, each measured in the vintage available the day before that month’s decision. The signal does not set portfolio weights.

The saved observations span August 2024 through September 2026. This sample is too short to establish
predictive value. The same-day option is a historical comparison.''')
st.caption('Independent course app inspired by FRED; not affiliated with the Federal Reserve. AI assistance: Codex helped build the app and checks.')
