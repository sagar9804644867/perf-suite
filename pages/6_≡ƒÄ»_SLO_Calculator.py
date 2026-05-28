import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SLI/SLO Calculator", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #22d3ee;
                      border-bottom: 1px solid #2d4a6e; padding-bottom: 8px; margin: 20px 0 15px 0; }
    .slo-card { background: linear-gradient(135deg, #1a2035, #1f2d45);
                border-radius: 12px; padding: 20px; text-align: center; margin: 6px 0; }
    .slo-val  { font-size: 2rem; font-weight: 800; margin: 0; }
    .slo-lbl  { font-size: 0.78rem; color: #94a3b8; text-transform: uppercase; }
    h1,h2,h3  { color: #e2e8f0 !important; }
    .stNumberInput input { background-color: #1a2035 !important; color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 SLI/SLO Calculator")
    st.markdown("---")
    st.markdown("### 📖 Definitions")
    st.markdown("""
**SLI** — Service Level Indicator
Actual measured metric (e.g. 99.5% uptime)

**SLO** — Service Level Objective
Target you want to achieve (e.g. 99.9% uptime)

**SLA** — Service Level Agreement
Contract with consequences if SLO is missed

**Error Budget** = 100% - SLO target
Amount of downtime/errors you can afford
    """)

st.markdown("# 🎯 SLI/SLO Calculator & Error Budget Tracker")
st.markdown("**Define SLOs, calculate error budgets, track burn rate and compliance status**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Availability SLO", "⏱️ Latency SLO", "❌ Error Rate SLO"])

with tab1:
    st.markdown('<p class="section-header">📊 Availability SLO Calculator</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        slo_target    = st.number_input("SLO Target (%)", value=99.9, min_value=90.0, max_value=99.999, step=0.001, format="%.3f")
        period_days   = st.number_input("Period (days)", value=30, min_value=1, max_value=365)
    with c2:
        actual_uptime = st.number_input("Actual Uptime (%)", value=99.95, min_value=0.0, max_value=100.0, step=0.001, format="%.3f")
        downtime_mins = st.number_input("Downtime this period (minutes)", value=15.0, step=1.0)
    with c3:
        st.markdown("**SLO Presets:**")
        preset = st.selectbox("Quick select", ["Custom", "99.9% (Three Nines)", "99.95%", "99.99% (Four Nines)", "99.999% (Five Nines)"])
        if preset != "Custom":
            preset_map = {"99.9% (Three Nines)": 99.9, "99.95%": 99.95, "99.99% (Four Nines)": 99.99, "99.999% (Five Nines)": 99.999}
            slo_target = preset_map[preset]

    # Calculations
    total_mins         = period_days * 24 * 60
    error_budget_mins  = total_mins * (1 - slo_target/100)
    used_mins          = downtime_mins
    remaining_mins     = max(0, error_budget_mins - used_mins)
    burn_rate          = (used_mins / error_budget_mins * 100) if error_budget_mins > 0 else 0
    compliance         = actual_uptime >= slo_target

    st.markdown("<br>", unsafe_allow_html=True)
    k1,k2,k3,k4,k5 = st.columns(5)
    metrics = [
        (f"{error_budget_mins:.1f}m", "Error Budget", "#22d3ee"),
        (f"{used_mins:.1f}m", "Used", "#ef4444" if burn_rate > 80 else "#f59e0b"),
        (f"{remaining_mins:.1f}m", "Remaining", "#22c55e" if remaining_mins > 0 else "#ef4444"),
        (f"{burn_rate:.1f}%", "Burn Rate", "#ef4444" if burn_rate > 100 else "#f59e0b" if burn_rate > 50 else "#22c55e"),
        ("✅ PASS" if compliance else "❌ FAIL", "SLO Status", "#22c55e" if compliance else "#ef4444"),
    ]
    for col, (val, lbl, color) in zip([k1,k2,k3,k4,k5], metrics):
        with col:
            st.markdown(f'<div class="slo-card" style="border:1px solid {color}"><p class="slo-val" style="color:{color}">{val}</p><p class="slo-lbl">{lbl}</p></div>', unsafe_allow_html=True)

    # Nines reference table
    st.markdown('<p class="section-header">📋 Downtime Allowance Reference</p>', unsafe_allow_html=True)
    nines_data = {
        "SLO": ["99%", "99.5%", "99.9%", "99.95%", "99.99%", "99.999%"],
        "Downtime/Day": ["14.4 min", "7.2 min", "1.44 min", "43.2 sec", "8.64 sec", "0.86 sec"],
        "Downtime/Month": ["7.3 hr", "3.6 hr", "43.8 min", "21.9 min", "4.38 min", "26.3 sec"],
        "Downtime/Year": ["87.6 hr", "43.8 hr", "8.77 hr", "4.38 hr", "52.6 min", "5.26 min"],
        "Called": ["Two Nines", "Two Half", "Three Nines", "Three Half", "Four Nines", "Five Nines"],
    }
    df_nines = pd.DataFrame(nines_data)
    st.dataframe(df_nines, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<p class="section-header">⏱️ Latency SLO Calculator</p>', unsafe_allow_html=True)
    lc1, lc2 = st.columns(2)
    with lc1:
        p99_slo     = st.number_input("P99 Latency SLO (ms)", value=2000, step=100)
        p95_slo     = st.number_input("P95 Latency SLO (ms)", value=1500, step=100)
        p90_slo     = st.number_input("P90 Latency SLO (ms)", value=1000, step=100)
    with lc2:
        actual_p99  = st.number_input("Actual P99 (ms)", value=1800, step=100)
        actual_p95  = st.number_input("Actual P95 (ms)", value=1200, step=100)
        actual_p90  = st.number_input("Actual P90 (ms)", value=800, step=100)

    latency_checks = [
        ("P90", p90_slo, actual_p90),
        ("P95", p95_slo, actual_p95),
        ("P99", p99_slo, actual_p99),
    ]

    fig = go.Figure()
    for pct, slo, actual in latency_checks:
        color = "#22c55e" if actual <= slo else "#ef4444"
        fig.add_trace(go.Bar(name=f"{pct} Actual", x=[pct], y=[actual], marker_color=color))
        fig.add_trace(go.Bar(name=f"{pct} SLO", x=[pct], y=[slo], marker_color="#2d4a6e", opacity=0.5))

    fig.update_layout(
        template="plotly_dark", paper_bgcolor="#1a2035", plot_bgcolor="#1a2035",
        height=350, margin=dict(l=10,r=10,t=10,b=10),
        barmode="group", yaxis_title="Latency (ms)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig, use_container_width=True)

    for pct, slo, actual in latency_checks:
        status = "✅ PASS" if actual <= slo else "❌ BREACH"
        color  = "#22c55e" if actual <= slo else "#ef4444"
        headroom = slo - actual
        st.markdown(f"**{pct}:** Actual `{actual}ms` vs SLO `{slo}ms` → <span style='color:{color}'>{status}</span> | Headroom: `{headroom}ms`", unsafe_allow_html=True)

with tab3:
    st.markdown('<p class="section-header">❌ Error Rate SLO Calculator</p>', unsafe_allow_html=True)
    ec1, ec2 = st.columns(2)
    with ec1:
        error_slo_pct    = st.number_input("Error Rate SLO (%)", value=1.0, step=0.1, format="%.2f")
        total_requests   = st.number_input("Total Requests", value=100000, step=1000)
    with ec2:
        actual_errors    = st.number_input("Actual Errors", value=450, step=10)
        period_label     = st.selectbox("Period", ["Last Hour", "Last Day", "Last Week", "Last Month"])

    actual_error_pct = (actual_errors / total_requests * 100) if total_requests > 0 else 0
    error_budget_requests = total_requests * (error_slo_pct / 100)
    errors_remaining = max(0, error_budget_requests - actual_errors)
    compliance = actual_error_pct <= error_slo_pct

    ek1, ek2, ek3, ek4 = st.columns(4)
    error_metrics = [
        (f"{actual_error_pct:.3f}%", "Actual Error Rate", "#ef4444" if not compliance else "#22c55e"),
        (f"{error_slo_pct:.2f}%", "SLO Target", "#22d3ee"),
        (f"{errors_remaining:.0f}", "Errors Remaining in Budget", "#22c55e" if errors_remaining > 0 else "#ef4444"),
        ("✅ PASS" if compliance else "❌ BREACH", "Status", "#22c55e" if compliance else "#ef4444"),
    ]
    for col, (val, lbl, color) in zip([ek1,ek2,ek3,ek4], error_metrics):
        with col:
            st.markdown(f'<div class="slo-card" style="border:1px solid {color}"><p class="slo-val" style="color:{color}">{val}</p><p class="slo-lbl">{lbl}</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Built by **Sagar Chaudhary** | Performance Engineering Lead @ PwC India")
