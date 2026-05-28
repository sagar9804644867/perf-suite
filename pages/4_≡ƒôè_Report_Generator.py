import streamlit as st

st.set_page_config(page_title="Performance Report Generator", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    h1,h2,h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📊 Performance Test Report Generator")
st.markdown("**Upload JTL → Get professional HTML report with P90/P95/P99 charts and SLO validation**")
st.markdown("---")

st.link_button("📊 Open Report Generator",
               "https://perf-report-generator-rgggaruqln9gjmdlzvjhej.streamlit.app",
               use_container_width=True, type="primary")

st.markdown("---")
st.markdown("### 📋 What the report includes")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
- ✅ KPI summary (Avg, P90, P95, P99)
- ✅ SLO PASS/FAIL per transaction
- ✅ Error breakdown by response code
- ✅ Throughput per endpoint
    """)
with col2:
    st.markdown("""
- ✅ Response time trend chart
- ✅ Interactive Plotly charts
- ✅ Downloadable HTML report
- ✅ CSV summary export
    """)

st.markdown("---")
st.caption("Built by **Sagar Chaudhary** | Performance Engineering Lead @ PwC India")
