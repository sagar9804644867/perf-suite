import streamlit as st

st.set_page_config(
    page_title="Performance Engineering Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    .main  { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .tool-card {
        background: linear-gradient(135deg, #1a2035 0%, #1f2d45 100%);
        border: 1px solid #2d4a6e; border-radius: 14px;
        padding: 24px; margin: 8px 0; cursor: pointer;
        transition: all 0.3s;
    }
    .tool-card:hover { border-color: #22d3ee; }
    .tool-title { font-size: 1.1rem; font-weight: 700; color: #22d3ee; margin-bottom: 6px; }
    .tool-desc  { font-size: 0.85rem; color: #94a3b8; }
    .tool-tags  { margin-top: 10px; }
    .tag { display: inline-block; padding: 2px 8px; border-radius: 10px;
           font-size: 0.72rem; margin: 2px; font-weight: 600; }
    .tag-green  { background: #052e16; color: #22c55e; border: 1px solid #22c55e; }
    .tag-blue   { background: #172554; color: #60a5fa; border: 1px solid #60a5fa; }
    .tag-purple { background: #1e1b4b; color: #a78bfa; border: 1px solid #a78bfa; }
    .tag-orange { background: #1c1917; color: #fb923c; border: 1px solid #fb923c; }
    .tag-red    { background: #450a0a; color: #f87171; border: 1px solid #f87171; }
    .tag-teal   { background: #042f2e; color: #2dd4bf; border: 1px solid #2dd4bf; }
    .kpi-card { background: linear-gradient(135deg, #1a2035 0%, #1f2d45 100%);
                border: 1px solid #2d4a6e; border-radius: 12px;
                padding: 20px; text-align: center; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #22d3ee; margin: 0; }
    .kpi-label { font-size: 0.78rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    h1, h2, h3 { color: #e2e8f0 !important; }
    .hero-title { font-size: 2.8rem; font-weight: 800; color: #22d3ee; margin-bottom: 10px; }
    .hero-sub   { font-size: 1.1rem; color: #94a3b8; margin-bottom: 30px; }
    .divider { border-top: 1px solid #2d4a6e; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 Perf Suite")
    st.markdown("*by Sagar Chaudhary*")
    st.markdown("*Performance Engineer*")
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    st.markdown("Use the **pages** above to navigate to each tool.")
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[🌐 Portfolio](https://sagar-portfolio-new.vercel.app)")
    st.markdown("[💼 LinkedIn](https://linkedin.com/in/sagar-chaudhary-024254130)")
    st.markdown("[💻 GitHub](https://github.com/sagar9804644867)")
    st.markdown("---")
    st.markdown("### 📊 Suite Stats")
    st.markdown("**7 Tools** | **Free** | **No sign-up**")

# ── Hero ───────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 40px 0 20px 0;'>
    <p style='font-size:3.5rem; margin:0;'>🚀</p>
    <p class='hero-title'>Performance Engineering Suite</p>
    <p class='hero-sub'>The most comprehensive free performance testing toolkit — backend load testing,<br>
    frontend Lighthouse audits, AI script generation, LLM observability, and more.</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Bar ────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
with k1:
    st.markdown('<div class="kpi-card"><p class="kpi-value">7</p><p class="kpi-label">Tools</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi-card"><p class="kpi-value">Free</p><p class="kpi-label">Always</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi-card"><p class="kpi-value">0</p><p class="kpi-label">Sign-up needed</p></div>', unsafe_allow_html=True)
with k4:
    st.markdown('<div class="kpi-card"><p class="kpi-value">JMX</p><p class="kpi-label">Ready output</p></div>', unsafe_allow_html=True)
with k5:
    st.markdown('<div class="kpi-card"><p class="kpi-value">AI</p><p class="kpi-label">Powered</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Tools Grid ─────────────────────────────────────────────────
st.markdown("## 🛠️ Choose Your Tool")
st.markdown("*Click any tool in the sidebar to get started*")
st.markdown("<br>", unsafe_allow_html=True)

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🔧 JMeter AI Script Generator</div>
        <div class="tool-desc">Generate production-ready JMeter JMX scripts with full correlation engine.
        Supports REST, GraphQL, CSRF, session tokens, boundary extractors, JSR223 preprocessors and more.
        Auto-detects dynamic values from response samples.</div>
        <div class="tool-tags">
            <span class="tag tag-green">JSON Extractor</span>
            <span class="tag tag-blue">RegEx Extractor</span>
            <span class="tag tag-orange">Boundary Extractor</span>
            <span class="tag tag-purple">GraphQL</span>
            <span class="tag tag-teal">JSR223</span>
            <span class="tag tag-red">CSRF</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🧠 Natural Language → JMeter</div>
        <div class="tool-desc">Describe your performance test in plain English and get a complete JMX script.
        Powered by Claude AI. Detects user flows, correlations, CSV requirements and SLA thresholds automatically.
        5 built-in example templates.</div>
        <div class="tool-tags">
            <span class="tag tag-purple">Claude AI</span>
            <span class="tag tag-green">Auto Correlation</span>
            <span class="tag tag-blue">Plain English</span>
            <span class="tag tag-orange">Banking</span>
            <span class="tag tag-teal">GraphQL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">⚡ LLM Performance Dashboard</div>
        <div class="tool-desc">Benchmark and compare 5 LLM models — GPT-4o, Claude 3 Haiku, Claude 3 Sonnet,
        GPT-4o-mini, and Gemini 1.5 Flash. Track TTFT, P99 latency, token throughput,
        cost per 1K tokens with configurable SLO thresholds.</div>
        <div class="tool-tags">
            <span class="tag tag-green">TTFT</span>
            <span class="tag tag-blue">P99 Latency</span>
            <span class="tag tag-purple">Token Cost</span>
            <span class="tag tag-orange">SLO Tracking</span>
            <span class="tag tag-teal">5 LLM Models</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">📊 Performance Test Report Generator</div>
        <div class="tool-desc">Upload your JMeter JTL file and instantly generate a professional HTML report.
        Shows P50/P95/P99 latency, error breakdown by transaction, throughput charts,
        SLO PASS/FAIL validation and downloadable HTML report.</div>
        <div class="tool-tags">
            <span class="tag tag-green">JTL Upload</span>
            <span class="tag tag-blue">P90/P95/P99</span>
            <span class="tag tag-orange">SLO Validation</span>
            <span class="tag tag-purple">HTML Report</span>
            <span class="tag tag-teal">CSV Export</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 3
col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🌐 UI Performance Analyzer (Lighthouse)</div>
        <div class="tool-desc">Analyze frontend performance using Google Lighthouse metrics.
        Enter any URL to get Core Web Vitals scores — LCP, FCP, CLS, INP, TTI, TBT.
        Compare before/after, get actionable recommendations and SEO impact analysis.</div>
        <div class="tool-tags">
            <span class="tag tag-green">Core Web Vitals</span>
            <span class="tag tag-blue">LCP / FCP / CLS</span>
            <span class="tag tag-purple">INP / TTI</span>
            <span class="tag tag-orange">SEO Impact</span>
            <span class="tag tag-red">Lighthouse Score</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🎯 SLI/SLO Calculator & Error Budget</div>
        <div class="tool-desc">Define your Service Level Objectives, calculate error budgets,
        track burn rate and get PASS/FAIL compliance status. Supports availability,
        latency, and error rate SLOs with real-time budget remaining calculations.</div>
        <div class="tool-tags">
            <span class="tag tag-green">Error Budget</span>
            <span class="tag tag-blue">Burn Rate</span>
            <span class="tag tag-purple">SLO Compliance</span>
            <span class="tag tag-orange">Availability</span>
            <span class="tag tag-teal">P99 Latency SLO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 4 - JTL Comparator
col7, col8 = st.columns(2)
with col7:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🔄 JTL Comparator</div>
        <div class="tool-desc">Upload two JMeter JTL files and compare test runs side by side.
        See which transactions improved or degraded, with percentage change analysis,
        P90/P95/P99 comparison charts and overall health score delta.</div>
        <div class="tool-tags">
            <span class="tag tag-green">Before vs After</span>
            <span class="tag tag-blue">% Change</span>
            <span class="tag tag-purple">Regression Detection</span>
            <span class="tag tag-orange">P99 Comparison</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🧵 Thread Group Calculator</div>
        <div class="tool-desc">Calculate optimal JMeter thread count from your target TPS and response time.
        Uses Little's Law: Threads = TPS × Response Time. Input your SLA requirements
        and get recommended thread count, ramp-up and duration settings.</div>
        <div class="tool-tags">
            <span class="tag tag-green">Little's Law</span>
            <span class="tag tag-blue">TPS Calculator</span>
            <span class="tag tag-purple">Ramp-up Advisor</span>
            <span class="tag tag-orange">Capacity Planning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Why This Suite ─────────────────────────────────────────────
st.markdown("## 💡 Why This Suite?")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    **🆓 Completely Free**
    No subscription. No sign-up. No credit card.
    Every tool is open source and free forever.
    """)
with c2:
    st.markdown("""
    **🤖 AI-Powered**
    Tools use Claude AI for intelligent JMX generation,
    correlation detection, and test design.
    """)
with c3:
    st.markdown("""
    **🏗️ Built from Real Experience**
    Built by a Performance Engineer with 5.6 years
    across PwC, TCS, Capgemini, and Wipro.
    """)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("Built by **Sagar Chaudhary** | Performance Engineer | [Portfolio](https://sagar-portfolio-new.vercel.app) | [LinkedIn](https://linkedin.com/in/sagar-chaudhary-024254130) | [GitHub](https://github.com/sagar9804644867)")
