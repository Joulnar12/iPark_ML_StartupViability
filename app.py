import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="iPark Viability Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #faf9f7; color: #1a1a1a; }
.main { background: #faf9f7 !important; }
.block-container { padding: 2rem 2.5rem !important; max-width: 100% !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #6b1a2a 0%, #4a1020 100%) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * { color: #f5e6e8 !important; }
section[data-testid="stSidebar"] label { color: #f5e6e8 !important; font-size: 12px !important; letter-spacing: 0.04em !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #f5e6e8 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #f5e6e8 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stSlider > div > div > div { background: #e8a0aa !important; }
section[data-testid="stSidebar"] .stSlider span,
section[data-testid="stSidebar"] .stSlider p,
section[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMin"],
section[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMax"] {
    background: transparent !important;
    background-color: transparent !important;
    color: rgba(255,255,255,0.4) !important;
    font-size: 10px !important;
}
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
section[data-testid="stSidebar"] h2 { color: white !important; font-family: 'Playfair Display', serif !important; }
section[data-testid="stSidebar"] h3 { color: rgba(255,255,255,0.6) !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 0.08em; }
section[data-testid="stSidebar"] p { color: rgba(255,255,255,0.5) !important; }

.about-card {
    background: white;
    border: 1px solid #ece9e4;
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.about-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #6b1a2a, #c8455a);
}
.about-icon { font-size: 20px; margin-bottom: 8px; }
.about-title { font-family: 'Playfair Display', serif; font-size: 18px; font-weight: 700; margin-bottom: 10px; color: #1a1a1a; }
.about-text { font-size: 13px; color: #666; line-height: 1.7; margin-bottom: 1.5rem; }
.about-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; }
.about-item { background: #faf9f7; border-radius: 10px; padding: 1rem; }
.about-item-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: #999; margin-bottom: 6px; }
.about-item-val { font-size: 13px; font-weight: 500; color: #1a1a1a; line-height: 1.5; }

.hero {
    background: linear-gradient(135deg, #6b1a2a 0%, #4a1020 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    right: -60px; top: -60px;
    width: 250px; height: 250px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero-name { font-family:'Playfair Display',serif; font-size:2.5rem; font-weight:700; color:white; line-height:1; }
.hero-sub { font-size:12px; color:rgba(255,255,255,0.45); margin-top:6px; letter-spacing:0.06em; text-transform:uppercase; }
.hero-badge { font-size:12px; font-weight:600; padding:8px 20px; border-radius:100px; letter-spacing:0.06em; text-transform:uppercase; }

.metric { background:white; border:1px solid #ece9e4; border-radius:16px; padding:1.5rem; position:relative; overflow:hidden; }
.metric::after { content:''; position:absolute; bottom:0;left:0;right:0; height:3px; background:var(--a,#6b1a2a); }
.metric-label { font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#aaa; margin-bottom:8px; }
.metric-val { font-family:'Playfair Display',serif; font-size:2.4rem; font-weight:700; line-height:1; }
.metric-desc { font-size:11px; color:#ccc; margin-top:6px; }

.sec-title { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:0.14em; color:#aaa; margin-bottom:1rem; padding-bottom:0.5rem; border-bottom:1px solid #ece9e4; }

.rbar { margin-bottom:0.85rem; }
.rbar-head { display:flex; justify-content:space-between; margin-bottom:6px; }
.rbar-label { font-size:13px; font-weight:500; color:#333; }
.rbar-val { font-size:12px; color:#aaa; }
.rbar-track { height:5px; background:#f0ede8; border-radius:3px; }
.rbar-fill { height:100%; border-radius:3px; }

.tag-row { display:flex; flex-wrap:wrap; gap:7px; }
.tg { font-size:11px; padding:4px 12px; border-radius:100px; font-weight:500; }
.tg-g { background:rgba(5,150,105,0.08); color:#059669; border:1px solid rgba(5,150,105,0.2); }
.tg-r { background:rgba(220,38,38,0.08); color:#dc2626; border:1px solid rgba(220,38,38,0.2); }

.vbar-row { margin-bottom:12px; }
.vbar-head { display:flex; justify-content:space-between; font-size:12px; color:#aaa; margin-bottom:6px; }
.vbar-track { height:7px; background:#f0ede8; border-radius:4px; }
.vbar-fill { height:100%; border-radius:4px; }

.rec { background:white; border:1px solid #ece9e4; border-radius:16px; padding:1.5rem; border-top:3px solid var(--c,#6b1a2a); height:100%; }
.rec-num { font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#bbb; margin-bottom:6px; }
.rec-title { font-family:'Playfair Display',serif; font-size:15px; font-weight:700; margin-bottom:3px; }
.rec-sub { font-size:11px; color:#bbb; margin-bottom:12px; font-style:italic; }
.rec-act { font-size:12px; color:#555; padding:4px 0; border-bottom:1px solid #f5f2ee; }
.rec-act:last-child { border-bottom:none; }
.rec-act::before { content:'→ '; color:#6b1a2a; font-weight:600; }

.footer { text-align:center; font-size:11px; color:#ccc; padding:2rem 0 1rem; letter-spacing:0.04em; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    clf      = joblib.load('rf_model.pkl')
    FEATURES = joblib.load('features.pkl')
    df       = pd.read_csv('startup_data.csv')
    df['reached_series_b'] = ((df['has_roundB']==1)|(df['has_roundC']==1)).astype(int)
    return clf, df, FEATURES

clf, df, FEATURES = load_model()

# ── Data ──────────────────────────────────────────────────────────────
LEBANON_RISKS = {
    'relationships':          {'hani':'Co-founder conflict (slide #2)',            'w':1.50},
    'milestones':             {'hani':'Market turmoil + No market interest (#4+6)','w':1.45},
    'funding_rounds':         {'hani':'Lack of VC + No pre-seed funds (#7+8)',     'w':1.40},
    'is_top500':              {'hani':'Lack of growth mindset (slide #3)',          'w':1.40},
    'reached_series_b':       {'hani':'Founders never get to market (slide #10)',  'w':1.30},
    'age_first_funding_year': {'hani':'Unclear direction (slide #11)',              'w':1.20},
}

RECS = {
    'relationships':          {'t':'Network & Team Risk',    'c':'#8b5cf6','s':'Amplified by brain drain',              'a':['Apply to iPark mentorship network — 50+ mentors by 2027','Target diaspora via iPark Global Bridge Program','Establish co-founder agreements early','Recruit remote diaspora talent']},
    'milestones':             {'t':'Market Validation Risk', 'c':'#d97706','s':'Amplified by purchasing power collapse', 'a':['Validate with dollar-paying customers first','Price in USD not LBP','Target MENA/EU market from day 1','Pursue iPark AIM program for validation']},
    'age_first_funding_year': {'t':'Timing Risk',            'c':'#059669','s':'Amplified by macro instability',         'a':['Define 12-month milestones only','Track 3 metrics: revenue, users, burn','Document pivot criteria in advance','Attend iPark pitch clinics (8+/year)']},
    'is_top500':              {'t':'Ecosystem Risk',         'c':'#0891b2','s':'Amplified by weak accelerator network',  'a':['Apply to iPark BDD incubation program','Consider Cyprus via iPark Mediterraneo','Apply to EU Horizon grants','Join Flat6Labs or Wamda']},
    'funding_rounds':         {'t':'Funding Access Risk',    'c':'#dc2626','s':'Amplified by VC collapse',               'a':['Target diaspora investors via iPark Global Bridge','Apply to EU Horizon grants (non-dilutive)','Consider revenue-based financing','Set up Stripe Atlas or Wise Business']},
    'reached_series_b':       {'t':'Execution Risk',         'c':'#2563eb','s':'Amplified by infrastructure failure',    'a':['Use cloud infrastructure — avoid physical servers','Build resilience plan for power outages','Establish international banking early','Consider Cyprus entity for international ops']},
}

LABELS = {
    'relationships':'Team Network','milestones':'Milestones',
    'funding_rounds':'Funding Rounds','is_top500':'Top Accelerator',
    'reached_series_b':'Series B+','age_first_funding_year':'Funding Timing',
}

fmax = {
    'relationships':          df['relationships'].quantile(0.95),
    'milestones':             df['milestones'].quantile(0.95),
    'funding_rounds':         df['funding_rounds'].quantile(0.95),
    'is_top500':              1,
    'reached_series_b':       1,
    'age_first_funding_year': df['age_first_funding_year'].quantile(0.95),
}

fmed = {
    'relationships':          df['relationships'].median(),
    'milestones':             df['milestones'].median(),
    'funding_rounds':         df['funding_rounds'].median(),
    'is_top500':              df['is_top500'].median(),
    'reached_series_b':       df['reached_series_b'].median(),
    'age_first_funding_year': df['age_first_funding_year'].median(),
}

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 Startup Profile")
    st.markdown("---")
    sname  = st.text_input("Startup name", "My Startup")
    st.markdown("### Funding")
    fr     = st.slider("Funding rounds", 0, 10, 1)
    hvc    = st.selectbox("VC backing?",    ["No","Yes"])
    hang   = st.selectbox("Angel backing?", ["No","Yes"])
    hra    = st.selectbox("Series A?",      ["No","Yes"])
    hrb    = st.selectbox("Series B?",      ["No","Yes"])
    hrc    = st.selectbox("Series C?",      ["No","Yes"])
    hrd    = st.selectbox("Series D?",      ["No","Yes"])
    st.markdown("### Team & Network")
    rels   = st.slider("Professional connections", 0, 30, 3)
    top500 = st.selectbox("In top accelerator?", ["No","Yes"])
    st.markdown("### Product & Timing")
    ms     = st.slider("Milestones hit", 0, 8, 1)
    aff    = st.slider("Years to first funding", 0.0, 10.0, 1.0, 0.5)
    alf    = st.slider("Years to last funding",  0.0, 15.0, 2.0, 0.5)

# ── Compute ───────────────────────────────────────────────────────────
HVC=1 if hvc=="Yes" else 0; HANG=1 if hang=="Yes" else 0
HRA=1 if hra=="Yes" else 0; HRB=1 if hrb=="Yes" else 0
HRC=1 if hrc=="Yes" else 0; HRD=1 if hrd=="Yes" else 0
IS500=1 if top500=="Yes" else 0; RSB=int(HRB or HRC)

fv   = pd.DataFrame([[fr,HVC,HANG,HRA,HRB,HRC,HRD,ms,IS500,RSB,rels,aff,alf]],columns=FEATURES)
base = clf.predict_proba(fv)[0][1]*100

fvals = {'relationships':rels,'milestones':ms,'funding_rounds':fr,
         'is_top500':IS500,'reached_series_b':RSB,'age_first_funding_year':aff}

# Personal risk — deviation from median amplified by Lebanese weight
pr = {}
for feat, info in LEBANON_RISKS.items():
    val  = fvals[feat]
    mx   = fmax[feat]
    med  = fmed[feat]
    ns   = min(val / (mx + 1e-9), 1.0)
    # Extra penalty for being below dataset median
    below_median = max(0, (med - val) / (med + 1e-9)) * 0.3
    p_risk = (1 - ns + below_median) * (info['w'] - 1.0)
    pr[feat] = {'r': round(p_risk, 4), 'ns': round(ns, 3)}

pdf = pd.DataFrame({'Personal Risk':[pr[f]['r'] for f in pr],
                    'Norm Score':   [pr[f]['ns'] for f in pr]},
                   index=list(pr.keys())).sort_values('Personal Risk',ascending=False)

penalty  = pdf['Personal Risk'].sum()*25
adjusted = max(0, base-penalty)
gap      = base-adjusted
rl  = 'CRITICAL' if adjusted<30 else 'HIGH' if adjusted<45 else 'MODERATE' if adjusted<60 else 'GOOD'
rc  = {'GOOD':'#059669','MODERATE':'#d97706','HIGH':'#dc2626','CRITICAL':'#7c3aed'}[rl]
rbg = {'GOOD':'rgba(5,150,105,0.08)','MODERATE':'rgba(217,119,6,0.08)',
       'HIGH':'rgba(220,38,38,0.08)','CRITICAL':'rgba(124,58,237,0.08)'}[rl]

strengths = [f for f in pdf.index if pdf.loc[f,'Norm Score']>=0.6]
gaps_l    = [f for f in pdf.index if pdf.loc[f,'Norm Score']<0.4]
top3      = list(pdf.head(3).index)
maxr      = pdf['Personal Risk'].max()

# ── ABOUT ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-card">
    <div class="about-icon">💡</div>
    <div class="about-title">About the Viability Engine</div>
    <div class="about-text">
        This decision-support tool uses machine learning trained on 923 real startup outcomes
        to predict baseline viability, then applies a Lebanese risk amplification layer grounded
        in iPark's expert research (Haidar & Nohra, 2024) and peer-reviewed literature.
        The model achieves 80% AUC on held-out test data and confirms 6 of iPark's
        12 globally-identified failure reasons through data alone.
    </div>
    <div class="about-grid">
        <div class="about-item">
            <div class="about-item-label">Data Source</div>
            <div class="about-item-val">923 real startup outcomes · Verified acquisition and closure events · Global dataset</div>
        </div>
        <div class="about-item">
            <div class="about-item-label">ML Model</div>
            <div class="about-item-val">Random Forest · 80% AUC · 5-fold cross-validated · 13 features</div>
        </div>
        <div class="about-item">
            <div class="about-item-label">Lebanese Risk Layer</div>
            <div class="about-item-val">iPark expert research (Haidar & Nohra, 2024) + World Bank, KAS/Arabnet, AGBI literature</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div>
    <div class="hero-name">🚀 {sname}</div>
    <div class="hero-sub">iPark · AUB Innovation Park · Lebanese Startup Viability Assessment</div>
  </div>
  <span class="hero-badge" style="background:{rbg};color:{rc};border:1px solid {rc}33">{rl}</span>
</div>""", unsafe_allow_html=True)

# ── METRICS ───────────────────────────────────────────────────────────
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="metric" style="--a:#6b1a2a"><div class="metric-label">Baseline Viability</div><div class="metric-val" style="color:#6b1a2a">{base:.1f}%</div><div class="metric-desc">Global ML · Random Forest · AUC 80%</div></div>',unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric" style="--a:{rc}"><div class="metric-label">Lebanon-Adjusted Viability</div><div class="metric-val" style="color:{rc}">{adjusted:.1f}%</div><div class="metric-desc">After Lebanese risk amplification</div></div>',unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric" style="--a:#dc2626"><div class="metric-label">Lebanese Risk Penalty</div><div class="metric-val" style="color:#dc2626">−{gap:.1f}%</div><div class="metric-desc">Structural amplification of failure signals</div></div>',unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>",unsafe_allow_html=True)

# ── MIDDLE ────────────────────────────────────────────────────────────
left, right = st.columns([1.4,1])

with left:
    st.markdown('<div class="sec-title">Personal Risk Ranking</div>',unsafe_allow_html=True)
    st.caption("How Lebanon amplifies YOUR specific failure signals based on your inputs")
    for feat in pdf.index:
        rv  = float(pdf.loc[feat,'Personal Risk'])
        pct = (rv/maxr*100) if maxr>0 else 0
        col = RECS[feat]['c']
        lbl = LABELS.get(feat,feat)
        st.markdown(f"""
        <div class="rbar">
          <div class="rbar-head"><span class="rbar-label">{lbl}</span><span class="rbar-val">{rv:.3f}</span></div>
          <div class="rbar-track"><div class="rbar-fill" style="width:{pct}%;background:{col}"></div></div>
        </div>""",unsafe_allow_html=True)

with right:
    st.markdown('<div class="sec-title">Strengths</div>',unsafe_allow_html=True)
    if strengths:
        tags="".join([f'<span class="tg tg-g">✓ {LABELS.get(f,f)}</span>' for f in strengths])
        st.markdown(f'<div class="tag-row">{tags}</div>',unsafe_allow_html=True)
    else:
        st.markdown('<span style="font-size:12px;color:#bbb">No strong signals detected</span>',unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem'></div>",unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Gap Alerts</div>',unsafe_allow_html=True)
    if gaps_l:
        tags="".join([f'<span class="tg tg-r">△ {LABELS.get(f,f)}</span>' for f in gaps_l])
        st.markdown(f'<div class="tag-row">{tags}</div>',unsafe_allow_html=True)
    else:
        st.markdown('<span style="font-size:12px;color:#bbb">No critical gaps detected</span>',unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>",unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Viability Comparison</div>',unsafe_allow_html=True)
    st.markdown(f"""
    <div class="vbar-row">
      <div class="vbar-head"><span>Baseline (Global ML)</span><span style="color:#6b1a2a;font-weight:600">{base:.1f}%</span></div>
      <div class="vbar-track"><div class="vbar-fill" style="width:{base}%;background:#6b1a2a"></div></div>
    </div>
    <div class="vbar-row">
      <div class="vbar-head"><span>Lebanon Adjusted</span><span style="color:{rc};font-weight:600">{adjusted:.1f}%</span></div>
      <div class="vbar-track"><div class="vbar-fill" style="width:{adjusted}%;background:{rc}"></div></div>
    </div>""",unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>",unsafe_allow_html=True)

# ── RECOMMENDATIONS ───────────────────────────────────────────────────
st.markdown('<div class="sec-title">Top 3 Recommendations — based on your personal risk profile</div>',unsafe_allow_html=True)
st.caption("Ranked by your highest adjusted risk scores · Linked to iPark Lebanon research & programs")

rc1,rc2,rc3 = st.columns(3)
for i,(feat,col) in enumerate(zip(top3,[rc1,rc2,rc3]),1):
    rec   = RECS[feat]
    info  = LEBANON_RISKS[feat]
    score = float(pdf.loc[feat,'Personal Risk'])
    acts  = "".join([f'<div class="rec-act">{a}</div>' for a in rec['a']])
    with col:
        st.markdown(f"""
        <div class="rec" style="--c:{rec['c']}">
          <div class="rec-num">Priority #{i} · Risk score {score:.3f}</div>
          <div class="rec-title" style="color:{rec['c']}">{rec['t']}</div>
          <div class="rec-sub">{info['hani']}</div>
          {acts}
        </div>""",unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  iPark — Talal & Madiha Zein AUB Innovation Park &nbsp;·&nbsp;
  ML Model: Random Forest · AUC 80% · 923 global startups &nbsp;·&nbsp;
  Lebanese Risk Layer: Haidar & Nohra (2024) + Literature Review
</div>""",unsafe_allow_html=True)