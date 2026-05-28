import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(page_title="JTL Comparator", page_icon="🔄", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #22d3ee;
                      border-bottom: 1px solid #2d4a6e; padding-bottom: 8px; margin: 20px 0 15px 0; }
    .improved { color: #22c55e; font-weight: 700; }
    .degraded { color: #ef4444; font-weight: 700; }
    .neutral  { color: #94a3b8; }
    h1,h2,h3  { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

def parse_jtl(file):
    df = pd.read_csv(file)
    df["success"] = df["success"].astype(str).str.lower() == "true"
    df["elapsed"] = pd.to_numeric(df["elapsed"], errors="coerce")
    return df

def compute_stats(df):
    return df.groupby("label").agg(
        Samples=("elapsed","count"),
        Avg=("elapsed","mean"),
        Median=("elapsed","median"),
        P90=("elapsed", lambda x: x.quantile(0.90)),
        P95=("elapsed", lambda x: x.quantile(0.95)),
        P99=("elapsed", lambda x: x.quantile(0.99)),
        Min=("elapsed","min"),
        Max=("elapsed","max"),
        Errors=("success", lambda x: (~x).sum()),
    ).reset_index()

with st.sidebar:
    st.markdown("## 🔄 JTL Comparator")
    st.markdown("Compare two JMeter test runs to detect regressions or improvements.")
    st.markdown("---")
    st.markdown("### 🎨 Color coding")
    st.markdown("🟢 **Green** = Improved (faster/fewer errors)")
    st.markdown("🔴 **Red** = Degraded (slower/more errors)")
    st.markdown("⚪ **Grey** = No significant change")

st.markdown("# 🔄 JTL Comparator")
st.markdown("**Compare two JMeter test runs side by side — detect regressions and improvements**")
st.markdown("---")

col_u1, col_u2 = st.columns(2)
with col_u1:
    st.markdown('<p class="section-header">📂 Baseline (Before) JTL</p>', unsafe_allow_html=True)
    baseline_label = st.text_input("Label for baseline", value="Baseline", key="bl")
    baseline_file  = st.file_uploader("Upload baseline JTL", type=["jtl","csv"], key="bf")
with col_u2:
    st.markdown('<p class="section-header">📂 Candidate (After) JTL</p>', unsafe_allow_html=True)
    candidate_label = st.text_input("Label for candidate", value="Candidate", key="cl")
    candidate_file  = st.file_uploader("Upload candidate JTL", type=["jtl","csv"], key="cf")

use_sample = st.checkbox("Use sample data (demo mode)", value=True)

if use_sample:
    np.random.seed(42)
    labels = ["Login","Dashboard","Search","Checkout","Profile","Logout"]
    base_rows = []
    cand_rows = []
    for label in labels:
        base_lat = {"Login":800,"Dashboard":1200,"Search":600,"Checkout":1800,"Profile":500,"Logout":300}[label]
        cand_lat = int(base_lat * np.random.uniform(0.7, 1.3))
        for i in range(100):
            e_b = max(100, int(np.random.normal(base_lat, base_lat*0.15)))
            e_c = max(100, int(np.random.normal(cand_lat, cand_lat*0.15)))
            base_rows.append({"label":label,"elapsed":e_b,"success":np.random.random()>0.02})
            cand_rows.append({"label":label,"elapsed":e_c,"success":np.random.random()>0.02})
    df_base = pd.DataFrame(base_rows)
    df_cand = pd.DataFrame(cand_rows)
    st.info("📊 Using sample data — upload your own JTL files to compare real runs")
elif baseline_file and candidate_file:
    df_base = parse_jtl(baseline_file)
    df_cand = parse_jtl(candidate_file)
    st.success(f"✅ Baseline: {len(df_base):,} records | Candidate: {len(df_cand):,} records")
else:
    st.info("Upload both JTL files above or enable sample data to see comparison")
    st.stop()

# Compute stats
stats_base = compute_stats(df_base)
stats_cand = compute_stats(df_cand)

# Merge
merged = stats_base.merge(stats_cand, on="label", suffixes=(f"_{baseline_label}", f"_{candidate_label}"))

# P99 comparison chart
st.markdown('<p class="section-header">📊 P99 Latency Comparison</p>', unsafe_allow_html=True)
fig = go.Figure()
fig.add_trace(go.Bar(name=baseline_label,  x=merged["label"], y=merged[f"P99_{baseline_label}"],  marker_color="#22d3ee", opacity=0.85))
fig.add_trace(go.Bar(name=candidate_label, x=merged["label"], y=merged[f"P99_{candidate_label}"], marker_color="#f59e0b", opacity=0.85))
fig.update_layout(template="plotly_dark", paper_bgcolor="#1a2035", plot_bgcolor="#1a2035",
                  height=350, margin=dict(l=10,r=10,t=10,b=10), barmode="group",
                  yaxis_title="P99 Latency (ms)", legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

# Delta table
st.markdown('<p class="section-header">📋 Transaction-Level Comparison</p>', unsafe_allow_html=True)

rows = []
for _, row in merged.iterrows():
    p99_b = row[f"P99_{baseline_label}"]
    p99_c = row[f"P99_{candidate_label}"]
    avg_b = row[f"Avg_{baseline_label}"]
    avg_c = row[f"Avg_{candidate_label}"]
    err_b = row[f"Errors_{baseline_label}"]
    err_c = row[f"Errors_{candidate_label}"]
    samp_b = row[f"Samples_{baseline_label}"]
    samp_c = row[f"Samples_{candidate_label}"]

    p99_delta = ((p99_c - p99_b) / p99_b * 100) if p99_b > 0 else 0
    avg_delta = ((avg_c - avg_b) / avg_b * 100) if avg_b > 0 else 0
    err_pct_b = (err_b / samp_b * 100) if samp_b > 0 else 0
    err_pct_c = (err_c / samp_c * 100) if samp_c > 0 else 0

    verdict = "✅ Improved" if p99_delta < -5 else "❌ Degraded" if p99_delta > 5 else "➡️ No Change"

    rows.append({
        "Transaction": row["label"],
        f"P99 {baseline_label}": f"{p99_b:.0f}ms",
        f"P99 {candidate_label}": f"{p99_c:.0f}ms",
        "P99 Δ%": f"{p99_delta:+.1f}%",
        f"Avg {baseline_label}": f"{avg_b:.0f}ms",
        f"Avg {candidate_label}": f"{avg_c:.0f}ms",
        "Avg Δ%": f"{avg_delta:+.1f}%",
        f"Err% {baseline_label}": f"{err_pct_b:.2f}%",
        f"Err% {candidate_label}": f"{err_pct_c:.2f}%",
        "Verdict": verdict,
    })

df_comparison = pd.DataFrame(rows)
st.dataframe(df_comparison.set_index("Transaction"), use_container_width=True)

# Overall verdict
improved = sum(1 for r in rows if "Improved" in r["Verdict"])
degraded = sum(1 for r in rows if "Degraded" in r["Verdict"])

st.markdown('<p class="section-header">🏆 Overall Verdict</p>', unsafe_allow_html=True)
v1,v2,v3 = st.columns(3)
with v1: st.metric("✅ Improved", improved)
with v2: st.metric("❌ Degraded", degraded)
with v3: st.metric("➡️ No Change", len(rows)-improved-degraded)

if degraded == 0:
    st.success("🎉 No regressions detected! All transactions maintained or improved performance.")
elif degraded > improved:
    st.error(f"⚠️ {degraded} transactions degraded — performance regression detected! Review before releasing.")
else:
    st.warning(f"⚠️ {degraded} transactions degraded, {improved} improved. Mixed results — review degraded transactions.")

st.markdown("---")
st.caption("Built by **Sagar Chaudhary** | Performance Engineering Lead @ PwC India")
