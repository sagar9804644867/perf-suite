import streamlit as st

st.set_page_config(page_title="Natural Language to JMeter", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .tool-card { background: linear-gradient(135deg, #1a2035, #1f2d45);
                 border: 1px solid #22d3ee; border-radius: 14px; padding: 30px; margin: 20px 0; }
    h1,h2,h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🧠 Natural Language → JMeter")
st.markdown("**Describe your test in plain English — get a complete production-ready JMX**")
st.markdown("---")

st.info("💡 Requires your Anthropic API key — get free credits at console.anthropic.com")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### 💬 Example prompt:
    > *"Load test https://mybank.com with 500 users. Users login, extract the auth token,
    fetch account balance, transfer $100, and logout. Ramp up 2 minutes, run 10 minutes.
    SLA 3 seconds P99."*
    """)
with col2:
    st.markdown("""
    ### ✅ Auto-detects:
    - All user flow steps in order
    - Dynamic values needing correlation
    - Auth token extraction
    - CSV data requirements
    - SLA thresholds
    - Load parameters
    """)

st.link_button("🧠 Open NL to JMeter Tool",
               "https://nl-to-jmeter.streamlit.app",
               use_container_width=True, type="primary")

st.markdown("---")
st.caption("Built by **Sagar Chaudhary** | Performance Engineering Lead @ PwC India")
