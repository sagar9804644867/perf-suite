import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Thread Group Calculator", page_icon="🧵", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #22d3ee;
                      border-bottom: 1px solid #2d4a6e; padding-bottom: 8px; margin: 20px 0 15px 0; }
    .result-card { background: linear-gradient(135deg, #1a2035, #1f2d45);
                   border: 1px solid #22d3ee; border-radius: 12px;
                   padding: 24px; text-align: center; margin: 6px 0; }
    .result-val { font-size: 2.5rem; font-weight: 800; color: #22d3ee; margin: 0; }
    .result-lbl { font-size: 0.78rem; color: #94a3b8; text-transform: uppercase; }
    .formula-box { background: #1a2035; border: 1px solid #2d4a6e; border-radius: 8px;
                   padding: 16px; font-family: monospace; color: #22d3ee; }
    h1,h2,h3 { color: #e2e8f0 !important; }
    .stNumberInput input { background-color: #1a2035 !important; color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧵 Thread Calculator")
    st.markdown("---")
    st.markdown("### 📖 Little's Law")
    st.markdown("""
```
Threads = TPS × Response Time (s)
```

**Example:**
- Target: 100 TPS
- Response time: 2s
- Threads = 100 × 2 = **200 users**

**With think time:**
- Think time: 1s
- Threads = 100 × (2+1) = **300 users**
    """)
    st.markdown("---")
    st.markdown("### 📊 Ramp-up Rule")
    st.markdown("Ramp-up = 10× think time OR 1 user/sec — whichever is longer")

st.markdown("# 🧵 Thread Group Calculator")
st.markdown("**Calculate optimal JMeter thread count using Little's Law**")
st.markdown("---")

st.markdown('<p class="section-header">🎯 Test Requirements</p>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    target_tps    = st.number_input("Target TPS (transactions/sec)", value=100, min_value=1)
    avg_resp_time = st.number_input("Expected Avg Response Time (ms)", value=2000, step=100)
with c2:
    think_time    = st.number_input("Think Time (ms)", value=1000, step=100)
    test_duration = st.number_input("Test Duration (seconds)", value=300, step=60)
with c3:
    error_rate    = st.number_input("Acceptable Error Rate (%)", value=1.0, step=0.1)
    pct_type      = st.selectbox("Latency SLO type", ["P90", "P95", "P99"])
    latency_slo   = st.number_input(f"{pct_type} SLO (ms)", value=5000, step=500)

# Calculations
resp_time_s  = avg_resp_time / 1000
think_time_s = think_time / 1000
cycle_time_s = resp_time_s + think_time_s

# Little's Law
threads_littles = target_tps * cycle_time_s
threads_no_think = target_tps * resp_time_s

# Ramp-up recommendation
ramp_up_rec = max(threads_littles * 0.1, threads_littles / target_tps)

# Throughput check
actual_tps_check = threads_littles / cycle_time_s

st.markdown('<p class="section-header">📊 Calculated Thread Configuration</p>', unsafe_allow_html=True)
r1,r2,r3,r4 = st.columns(4)
results = [
    (f"{int(threads_littles)}", "Recommended Threads", "#22d3ee"),
    (f"{int(threads_no_think)}", "Min Threads (no think)", "#60a5fa"),
    (f"{int(ramp_up_rec)}s", "Recommended Ramp-up", "#f59e0b"),
    (f"{actual_tps_check:.1f}", "Achievable TPS", "#22c55e"),
]
for col, (val, lbl, color) in zip([r1,r2,r3,r4], results):
    with col:
        st.markdown(f'<div class="result-card"><p class="result-val" style="color:{color}">{val}</p><p class="result-lbl">{lbl}</p></div>', unsafe_allow_html=True)

# Formula display
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="section-header">🧮 Calculation Breakdown</p>', unsafe_allow_html=True)
st.markdown(f"""
<div class="formula-box">
Little's Law: Threads = TPS × Cycle Time<br>
<br>
Cycle Time = Response Time + Think Time<br>
           = {avg_resp_time}ms + {think_time}ms<br>
           = {avg_resp_time+think_time}ms = {cycle_time_s:.2f}s<br>
<br>
Threads = {target_tps} TPS × {cycle_time_s:.2f}s = <strong>{threads_littles:.1f} → Round up to {int(threads_littles)+1}</strong><br>
<br>
Recommended Ramp-up = {int(ramp_up_rec)} seconds<br>
Test Duration = {test_duration} seconds<br>
Achievable TPS = {int(threads_littles)} / {cycle_time_s:.2f}s = {actual_tps_check:.1f} TPS
</div>
""", unsafe_allow_html=True)

# JMeter config output
st.markdown('<p class="section-header">📋 JMeter Thread Group Configuration</p>', unsafe_allow_html=True)
jmeter_config = f"""
Thread Group Settings:
━━━━━━━━━━━━━━━━━━━━
Number of Threads (users):  {int(threads_littles)+1}
Ramp-up Period (seconds):   {int(ramp_up_rec)}
Duration (seconds):          {test_duration}
Scheduler:                   ✅ Enabled
Loop Count:                  -1 (Infinite)

Summary:
━━━━━━━━
Target TPS:       {target_tps}
Response Time:    {avg_resp_time}ms
Think Time:       {think_time}ms
Cycle Time:       {avg_resp_time+think_time}ms
Achievable TPS:   {actual_tps_check:.1f}
"""
st.code(jmeter_config)

# TPS vs Threads chart
st.markdown('<p class="section-header">📈 TPS vs Thread Count</p>', unsafe_allow_html=True)
thread_range = list(range(10, int(threads_littles)*2+10, max(1, int(threads_littles)//20)))
tps_range = [t / cycle_time_s for t in thread_range]

fig = go.Figure()
fig.add_trace(go.Scatter(x=thread_range, y=tps_range, mode="lines",
                         line=dict(color="#22d3ee", width=2), name="Achievable TPS"))
fig.add_vline(x=threads_littles, line_dash="dash", line_color="#f59e0b",
              annotation_text=f"Recommended: {int(threads_littles)} threads")
fig.add_hline(y=target_tps, line_dash="dash", line_color="#22c55e",
              annotation_text=f"Target: {target_tps} TPS")
fig.update_layout(template="plotly_dark", paper_bgcolor="#1a2035", plot_bgcolor="#1a2035",
                  height=300, margin=dict(l=10,r=10,t=10,b=10),
                  xaxis_title="Number of Threads", yaxis_title="TPS")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Built by **Sagar Chaudhary** | Performance Engineering Lead @ PwC India")
