import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="UI Performance Analyzer", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    div[data-testid="stSidebar"] { background-color: #0d1526; border-right: 1px solid #1e3a5f; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #22d3ee;
                      border-bottom: 1px solid #2d4a6e; padding-bottom: 8px; margin: 20px 0 15px 0; }
    .score-card { background: linear-gradient(135deg, #1a2035, #1f2d45);
                  border: 1px solid #2d4a6e; border-radius: 12px;
                  padding: 20px; text-align: center; }
    .score-val { font-size: 2.5rem; font-weight: 800; margin: 0; }
    .score-lbl { font-size: 0.78rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .metric-row { background: #1a2035; border-radius: 8px; padding: 12px 16px; margin: 6px 0; }
    .good    { color: #22c55e; }
    .needs   { color: #f59e0b; }
    .poor    { color: #ef4444; }
    h1,h2,h3 { color: #e2e8f0 !important; }
    .stTextInput input { background-color: #1a2035 !important; color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

def score_color(score):
    if score >= 90: return "#22c55e"
    if score >= 50: return "#f59e0b"
    return "#ef4444"

def score_label(score):
    if score >= 90: return "Good ✅"
    if score >= 50: return "Needs Improvement ⚠️"
    return "Poor ❌"

def metric_status(value, good_threshold, poor_threshold, unit="s", lower_is_better=True):
    if lower_is_better:
        if value <= good_threshold: return "good", f"✅ Good"
        if value <= poor_threshold: return "needs", f"⚠️ Needs Improvement"
        return "poor", f"❌ Poor"
    else:
        if value >= good_threshold: return "good", f"✅ Good"
        if value >= poor_threshold: return "needs", f"⚠️ Needs Improvement"
        return "poor", f"❌ Poor"

def fetch_pagespeed(url, strategy="mobile"):
    """Fetch Google PageSpeed Insights API data"""
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    api_key = st.sidebar.text_input("Google API Key (optional)", type="password", help="Get free key from console.developers.google.com")
    params = {
        "url": url,
        "strategy": strategy,
        "category": ["performance", "accessibility", "best-practices", "seo"],
        "key": api_key if api_key else None
    }
    try:
        resp = requests.get(api_url, params=params, timeout=60)
        if resp.status_code == 200:
            return resp.json(), None
        else:
            return None, f"API Error {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return None, str(e)

def parse_lighthouse_data(data):
    """Parse PageSpeed Insights response"""
    lhr = data.get("lighthouseResult", {})
    categories = lhr.get("categories", {})
    audits = lhr.get("audits", {})

    scores = {
        "Performance":     int((categories.get("performance", {}).get("score", 0) or 0) * 100),
        "Accessibility":   int((categories.get("accessibility", {}).get("score", 0) or 0) * 100),
        "Best Practices":  int((categories.get("best-practices", {}).get("score", 0) or 0) * 100),
        "SEO":             int((categories.get("seo", {}).get("score", 0) or 0) * 100),
    }

    # Core Web Vitals
    def get_metric(audit_id):
        audit = audits.get(audit_id, {})
        val = audit.get("numericValue", 0) or 0
        display = audit.get("displayValue", "N/A")
        score = audit.get("score", 0) or 0
        return {"value": val, "display": display, "score": score}

    metrics = {
        "FCP":  get_metric("first-contentful-paint"),
        "LCP":  get_metric("largest-contentful-paint"),
        "TBT":  get_metric("total-blocking-time"),
        "CLS":  get_metric("cumulative-layout-shift"),
        "SI":   get_metric("speed-index"),
        "TTI":  get_metric("interactive"),
    }

    # Opportunities
    opportunities = []
    for audit_id, audit in audits.items():
        if audit.get("details", {}).get("type") == "opportunity":
            savings = audit.get("details", {}).get("overallSavingsMs", 0) or 0
            if savings > 100:
                opportunities.append({
                    "title": audit.get("title", audit_id),
                    "description": audit.get("description", ""),
                    "savings_ms": savings,
                    "display": audit.get("displayValue", ""),
                })
    opportunities.sort(key=lambda x: x["savings_ms"], reverse=True)

    # Diagnostics
    diagnostics = []
    for audit_id, audit in audits.items():
        if audit.get("score") is not None and audit.get("score", 1) < 0.9:
            if audit.get("details", {}).get("type") not in ["opportunity"]:
                if audit.get("title"):
                    diagnostics.append({
                        "title": audit.get("title", ""),
                        "score": audit.get("score", 1),
                        "display": audit.get("displayValue", ""),
                    })

    return scores, metrics, opportunities[:8], diagnostics[:10]

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌐 UI Analyzer")
    st.markdown("*Powered by Google PageSpeed API*")
    st.markdown("---")
    st.markdown("### 📖 What it measures")
    st.markdown("""
**Core Web Vitals:**
- **LCP** — Largest Contentful Paint
- **FCP** — First Contentful Paint
- **CLS** — Cumulative Layout Shift
- **INP** — Interaction to Next Paint
- **TTI** — Time to Interactive
- **TBT** — Total Blocking Time

**Lighthouse Scores:**
- Performance (0-100)
- Accessibility (0-100)
- Best Practices (0-100)
- SEO (0-100)
    """)
    st.markdown("---")
    st.markdown("### 🆚 vs JMeter")
    st.markdown("""
| | Lighthouse | JMeter |
|--|--|--|
| Users | 1 | 1000s |
| Focus | UI quality | Load |
| SEO | ✅ | ❌ |
| APIs | ❌ | ✅ |
    """)

# ── Main ───────────────────────────────────────────────────────
st.markdown("# 🌐 UI Performance Analyzer")
st.markdown("**Google Lighthouse + PageSpeed Insights** — Analyze frontend performance, Core Web Vitals, and SEO impact")
st.markdown("---")

# URL Input
st.markdown('<p class="section-header">🔗 Enter URL to Analyze</p>', unsafe_allow_html=True)

col_u1, col_u2, col_u3 = st.columns([3, 1, 1])
with col_u1:
    url_input = st.text_input(
        "Website URL",
        placeholder="https://www.example.com",
        label_visibility="collapsed"
    )
with col_u2:
    strategy = st.selectbox("Device", ["mobile", "desktop"], label_visibility="collapsed")
with col_u3:
    analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)

# Compare mode
st.markdown('<p class="section-header">🆚 Compare Two URLs (Optional)</p>', unsafe_allow_html=True)
col_c1, col_c2 = st.columns(2)
with col_c1:
    compare_url = st.text_input("Compare with URL", placeholder="https://competitor.com", label_visibility="collapsed")
with col_c2:
    compare_btn = st.button("🔄 Compare Both", use_container_width=True)

# ── Analysis ───────────────────────────────────────────────────
def run_analysis(url, strategy, label=""):
    if not url.startswith("http"):
        url = "https://" + url

    with st.spinner(f"🔍 Running Lighthouse analysis for {url}..."):
        data, error = fetch_pagespeed(url, strategy)

    if error:
        st.error(f"❌ {error}")
        st.info("💡 This tool uses Google PageSpeed Insights API which is free and requires no API key.")
        return None

    scores, metrics, opportunities, diagnostics = parse_lighthouse_data(data)

    if label:
        st.markdown(f"### 📊 Results for: `{url}` {label}")

    # Lighthouse Scores
    st.markdown('<p class="section-header">🏆 Lighthouse Scores</p>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, (name, score) in zip([s1, s2, s3, s4], scores.items()):
        color = score_color(score)
        with col:
            st.markdown(f"""
            <div class="score-card">
                <p class="score-val" style="color:{color}">{score}</p>
                <p class="score-lbl">{name}</p>
                <p style="font-size:0.75rem; color:{color}">{score_label(score)}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Web Vitals
    st.markdown('<p class="section-header">⚡ Core Web Vitals</p>', unsafe_allow_html=True)

    cwv_data = {
        "FCP":  {"val": metrics["FCP"]["value"]/1000,  "unit": "s",  "good": 1.8, "poor": 3.0,  "desc": "First Contentful Paint — time to first content visible"},
        "LCP":  {"val": metrics["LCP"]["value"]/1000,  "unit": "s",  "good": 2.5, "poor": 4.0,  "desc": "Largest Contentful Paint — time to main content visible"},
        "TBT":  {"val": metrics["TBT"]["value"],       "unit": "ms", "good": 200, "poor": 600,  "desc": "Total Blocking Time — JS blocking main thread"},
        "CLS":  {"val": metrics["CLS"]["value"],       "unit": "",   "good": 0.1, "poor": 0.25, "desc": "Cumulative Layout Shift — visual stability"},
        "SI":   {"val": metrics["SI"]["value"]/1000,   "unit": "s",  "good": 3.4, "poor": 5.8,  "desc": "Speed Index — visual load progress"},
        "TTI":  {"val": metrics["TTI"]["value"]/1000,  "unit": "s",  "good": 3.8, "poor": 7.3,  "desc": "Time to Interactive — fully interactive"},
    }

    cv1, cv2, cv3 = st.columns(3)
    for i, (key, m) in enumerate(cwv_data.items()):
        col = [cv1, cv2, cv3][i % 3]
        status_class, status_text = metric_status(m["val"], m["good"], m["poor"])
        color = {"good": "#22c55e", "needs": "#f59e0b", "poor": "#ef4444"}[status_class]
        val_str = f"{m['val']:.2f}{m['unit']}"
        with col:
            st.markdown(f"""
            <div class="metric-row">
                <span style="color:#22d3ee; font-weight:700; font-size:1rem">{key}</span>
                <span style="color:{color}; font-weight:700; float:right">{val_str} {status_text}</span>
                <br><span style="color:#94a3b8; font-size:0.78rem">{m['desc']}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gauge chart
    st.markdown('<p class="section-header">📊 Performance Score Gauge</p>', unsafe_allow_html=True)
    perf_score = scores["Performance"]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=perf_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Performance Score — {strategy.title()}"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': score_color(perf_score)},
            'steps': [
                {'range': [0, 49],  'color': "#2d1010"},
                {'range': [50, 89], 'color': "#2d2010"},
                {'range': [90, 100],'color': "#102d10"},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': perf_score
            }
        }
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="#1a2035",
        height=300, margin=dict(l=30, r=30, t=50, b=10),
        font=dict(color="#e2e8f0")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Opportunities
    if opportunities:
        st.markdown('<p class="section-header">🚀 Top Optimization Opportunities</p>', unsafe_allow_html=True)
        for opp in opportunities[:6]:
            savings = opp["savings_ms"]
            color = "#22c55e" if savings < 500 else "#f59e0b" if savings < 2000 else "#ef4444"
            st.markdown(f"""
            <div class="metric-row">
                <span style="color:#e2e8f0; font-weight:600">{opp['title']}</span>
                <span style="color:{color}; float:right; font-weight:700">Save ~{savings:.0f}ms</span>
                <br><span style="color:#94a3b8; font-size:0.78rem">{opp['description'][:120]}...</span>
            </div>""", unsafe_allow_html=True)

    return scores, metrics

if analyze_btn and url_input:
    result = run_analysis(url_input, strategy)

elif compare_btn and url_input and compare_url:
    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        r1 = run_analysis(url_input, strategy, "🔵 URL 1")
    with col_r2:
        r2 = run_analysis(compare_url, strategy, "🟠 URL 2")

    if r1 and r2:
        st.markdown("---")
        st.markdown('<p class="section-header">🆚 Head-to-Head Comparison</p>', unsafe_allow_html=True)
        scores1, _ = r1
        scores2, _ = r2

        categories = list(scores1.keys())
        vals1 = list(scores1.values())
        vals2 = list(scores2.values())

        fig = go.Figure()
        fig.add_trace(go.Bar(name=url_input[:30], x=categories, y=vals1, marker_color="#22d3ee"))
        fig.add_trace(go.Bar(name=compare_url[:30], x=categories, y=vals2, marker_color="#f59e0b"))
        fig.add_hline(y=90, line_dash="dash", line_color="#22c55e", annotation_text="Good (90)")
        fig.add_hline(y=50, line_dash="dash", line_color="#f59e0b", annotation_text="Needs Improvement (50)")
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="#1a2035", plot_bgcolor="#1a2035",
            height=350, margin=dict(l=10,r=10,t=10,b=10),
            barmode="group", yaxis_title="Score", yaxis_range=[0,100],
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)

elif not url_input and (analyze_btn or compare_btn):
    st.warning("⚠️ Please enter a URL to analyze")

else:
    # Default state
    st.info("👆 Enter a URL above and click **Analyze** to get Lighthouse scores, Core Web Vitals, and optimization recommendations.")
    st.markdown("""
    **What you'll get:**
    - 🏆 Lighthouse scores (Performance, Accessibility, Best Practices, SEO)
    - ⚡ Core Web Vitals (LCP, FCP, CLS, TBT, TTI, Speed Index)
    - 🚀 Top optimization opportunities with estimated time savings
    - 📊 Visual gauge and comparison charts
    - 🆚 Side-by-side URL comparison mode
    """)

st.markdown("---")
st.caption("Powered by **Google PageSpeed Insights API** | Built by Sagar Chaudhary | [Portfolio](https://sagar-portfolio-new.vercel.app)")
