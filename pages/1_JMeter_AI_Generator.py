import streamlit as st

st.set_page_config(page_title="JMeter AI Script Generator", page_icon="🔧", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .tool-card { background: linear-gradient(135deg, #1a2035, #1f2d45);
                 border: 1px solid #22d3ee; border-radius: 14px; padding: 30px; margin: 20px 0; }
    h1,h2,h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔧 JMeter AI Script Generator")
st.markdown("**Full Correlation Engine v3.0** — JSON · RegEx · XPath · Boundary · CSRF · JSR223 · GraphQL")
st.markdown("---")

st.markdown("""
<div class="tool-card">
<h3>🚀 Launch the Full Tool</h3>
<p style="color:#94a3b8; font-size:1rem;">
The JMeter AI Script Generator is hosted as a standalone Streamlit app.<br>
Click the link below to open it in a new tab:
</p>
</div>
""", unsafe_allow_html=True)

st.link_button("🔧 Open JMeter AI Script Generator",
               "https://jmeter-ai-generator-ye7nzbuo8ctdj2esjwfulg.streamlit.app",
               use_container_width=True, type="primary")

st.markdown("---")
st.markdown("### ✅ What it generates")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
- ✅ Thread Group with scheduler
- ✅ HTTP Request Defaults
- ✅ Cookie + Cache Manager
- ✅ HTTP Header Manager
- ✅ HTTP Samplers (REST + GraphQL)
- ✅ CSV DataSet Config
- ✅ Loop Controller
    """)
with col2:
    st.markdown("""
- ✅ RegEx Extractor (JSON values)
- ✅ Boundary Extractor (server values)
- ✅ XPath Extractor (CSRF/HTML)
- ✅ JSR223 PreProcessor (Java)
- ✅ JSR223 PostProcessor (Java)
- ✅ Response + Duration Assertions
- ✅ Datadog Backend Listener
    """)

st.markdown("---")
st.caption("Built by **Sagar Chaudhary** | Performance Engineering Lead @ PwC India | [Portfolio](https://sagar-portfolio-new.vercel.app)")
