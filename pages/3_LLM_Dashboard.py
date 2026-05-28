import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="LLM Performance Dashboard", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #22d3ee;
                      border-bottom: 1px solid #2d4a6e; padding-bottom: 8px; margin: 20px 0 15px 0; }
    h1,h2,h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚡ LLM Performance Dashboard")
st.markdown("**Benchmark GPT-4o, Claude 3 Haiku, Gemini 1.5 Flash** — TTFT, Latency, Token Cost")
st.markdown("---")

st.link_button("⚡ Open Full LLM Dashboard",
               "https://llm-performance-dashboard-jcsucupcfsfaqpoqdbsr2k.streamlit.app",
               use_container_width=True, type="primary")

st.markdown("---")

# Quick preview chart
st.markdown('<p class="section-header">📊 Quick Preview — TTFT by Model</p>', unsafe_allow_html=True)

models = ["GPT-4o", "GPT-4o-mini", "Claude 3 Haiku", "Claude 3 Sonnet", "Gemini 1.5 Flash"]
ttft   = [1.8, 1.1, 0.7, 1.2, 0.9]
cost   = [0.030, 0.006, 0.004, 0.018, 0.005]
colors = ["#3b82f6","#8b5cf6","#22d3ee","#06b6d4","#f59e0b"]

fig = go.Figure()
fig.add_trace(go.Bar(x=models, y=ttft, marker_color=colors, name="Avg TTFT (s)"))
fig.add_hline(y=2.0, line_dash="dash", line_color="#ef4444", annotation_text="TTFT SLO (2s)")
fig.update_layout(template="plotly_dark", paper_bgcolor="#1a2035", plot_bgcolor="#1a2035",
                  height=300, margin=dict(l=10,r=10,t=10,b=10), yaxis_title="TTFT (seconds)")
st.plotly_chart(fig, use_container_width=True)

col1,col2,col3 = st.columns(3)
with col1: st.metric("Fastest TTFT", "Claude 3 Haiku (0.7s)")
with col2: st.metric("Lowest Cost", "Claude 3 Haiku ($0.004/1K)")
with col3: st.metric("Models Compared", "5")

st.markdown("---")
st.caption("Built by **Sagar Chaudhary** | Performance Engineering Lead @ PwC India")
