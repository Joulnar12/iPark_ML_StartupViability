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
.about-item-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: #777; margin-bottom: 6px; }
.about-item-val { font-size: 13px; font-weight: 500; color: #333; line-height: 1.5; }

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
.metric-label { font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#888; margin-bottom:8px; }
.metric-val { font-family:'Playfair Display',serif; font-size:2.4rem; font-weight:700; line-height:1; }
.metric-desc { font-size:11px; color:#888; margin-top:6px; }

.sec-title { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:0.14em; color:#777; margin-bottom:1rem; padding-bottom:0.5rem; border-bottom:1px solid #ece9e4; }

.rbar { margin-bottom:0.85rem; }
.rbar-head { display:flex; justify-content:space-between; margin-bottom:6px; }
.rbar-label { font-size:13px; font-weight:500; color:#333; }
.rbar-val { font-size:12px; color:#777; }
.rbar-track { height:5px; background:#f0ede8; border-radius:3px; }
.rbar-fill { height:100%; border-radius:3px; }

.tag-row { display:flex; flex-wrap:wrap; gap:7px; }
.tg { font-size:11px; padding:4px 12px; border-radius:100px; font-weight:500; }
.tg-g { background:rgba(5,150,105,0.08); color:#059669; border:1px solid rgba(5,150,105,0.2); }
.tg-r { background:rgba(220,38,38,0.08); color:#dc2626; border:1px solid rgba(220,38,38,0.2); }

.vbar-row { margin-bottom:12px; }
.vbar-head { display:flex; justify-content:space-between; font-size:12px; color:#666; margin-bottom:6px; }
.vbar-track { height:7px; background:#f0ede8; border-radius:4px; }
.vbar-fill { height:100%; border-radius:4px; }

.rec { background:white; border:1px solid #ece9e4; border-radius:16px; padding:1.5rem; border-top:3px solid var(--c,#6b1a2a); height:100%; }
.rec-num { font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#888; margin-bottom:6px; }
.rec-title { font-family:'Playfair Display',serif; font-size:15px; font-weight:700; margin-bottom:3px; }
.rec-sub { font-size:11px; color:#888; margin-bottom:12px; font-style:italic; }
.rec-act { font-size:12px; color:#444; padding:4px 0; border-bottom:1px solid #f5f2ee; }
.rec-act:last-child { border-bottom:none; }
.rec-act::before { content:'→ '; color:#6b1a2a; font-weight:600; }

.footer { text-align:center; font-size:11px; color:#888; padding:2rem 0 1rem; letter-spacing:0.04em; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    clf      = joblib.load('rf_model.pkl')
    FEATURES = joblib.load('features.pkl')
    df       = pd.read_csv('startup_data.csv')
    df['reached_series_b'] = ((df['has_roundB']==1)|(df['has_roundC']==1)).astype(int)
    return clf, df, FEATURES

clf, df, FEATURES = load_assets()

# ── Lebanese Risk Layer — exactly as in notebook ──────────────────────
LEBANON_RISKS = {
    'relationships': {
        'iPark_reason':  'Co-founder conflict (slide #2)',
        'iPark_weight':  1.5,
        'lit_evidence':  '875K left Lebanon 2019–2022. 63% talent emigrated.',
        'lit_weight':    1.5,
        'final_weight':  (1.5 + 1.5) / 2,
    },
    'is_top500': {
        'iPark_reason':  'Lack of growth mindset (slide #3)',
        'iPark_weight':  1.5,
        'lit_evidence':  '54.3% startups relocated. Ecosystem ranked #77 globally.',
        'lit_weight':    1.3,
        'final_weight':  (1.5 + 1.3) / 2,
    },
    'milestones': {
        'iPark_reason':  'Market turmoil + Lack of market interest (slides #4+6)',
        'iPark_weight':  1.4,
        'lit_evidence':  'Pound lost 90%+ value. Poverty jumped from 30% to 85–90%.',
        'lit_weight':    1.5,
        'final_weight':  (1.4 + 1.5) / 2,
    },
    'funding_rounds': {
        'iPark_reason':  'Lack of VC + No pre-seed funds (slides #7+8)',
        'iPark_weight':  1.3,
        'lit_evidence':  'Funding dropped 95% in 2023. Investment shrank 70% 2017–2021.',
        'lit_weight':    1.5,
        'final_weight':  (1.3 + 1.5) / 2,
    },
    'reached_series_b': {
        'iPark_reason':  'Founders never really get to market (slide #10)',
        'iPark_weight':  1.2,
        'lit_evidence':  '91.3% startups affected by infrastructure. 9h/day without electricity.',
        'lit_weight':    1.4,
        'final_weight':  (1.2 + 1.4) / 2,
    },
    'age_first_funding_year': {
        'iPark_reason':  'Unclear direction (slide #11)',
        'iPark_weight':  1.1,
        'lit_evidence':  'GDP shrank 53.4% 2019–2021. Top 3 worst crisis since mid-19th century.',
        'lit_weight':    1.3,
        'final_weight':  (1.1 + 1.3) / 2,
    },
}

# iPark failure reason color mapping (from notebook)
IPARK_COLORS = {
    'relationships':          '#8e44ad',   # ⑦ Not the right team
    'milestones':             '#e67e22',   # ② No market need
    'funding_rounds':         '#e74c3c',   # ① Ran out of cash
    'is_top500':              '#16a085',   # ③ Got outcompeted
    'reached_series_b':       '#2980b9',   # ④ Flawed business model
    'age_first_funding_year': '#27ae60',   # ⑧ Product mistimed
}

IPARK_REASONS = {
    'relationships':          '⑦ Not the right team',
    'milestones':             '② No market need',
    'funding_rounds':         '① Ran out of cash',
    'is_top500':              '③ Got outcompeted',
    'reached_series_b':       '④ Flawed business model',
    'age_first_funding_year': '⑧ Product mistimed',
}

FEATURE_LABELS = {
    'relationships':          'Team Network',
    'milestones':             'Milestones',
    'funding_rounds':         'Funding Rounds',
    'is_top500':              'Top Accelerator',
    'reached_series_b':       'Series B+',
    'age_first_funding_year': 'Funding Timing',
}

RECOMMENDATIONS = {
    'relationships': {
        'risk':    'Network & Team Risk — amplified by brain drain',
        'actions': [
            'Apply to iPark mentorship network — 50+ mentors by 2027 target',
            'Target diaspora connections via iPark Global Bridge Program',
            'Establish co-founder agreements early to reduce conflict risk',
            'Recruit remote diaspora talent — competitive at Lebanese market wages',
        ]
    },
    'milestones': {
        'risk':    'Market Validation Risk — amplified by purchasing power collapse',
        'actions': [
            'Validate with dollar-paying customers — diaspora or export market first',
            'Price in USD not LBP — protects against further devaluation',
            'Target MENA or EU market from day 1, use Lebanon as test bed only',
            'Pursue iPark AIM program for structured market validation support',
        ]
    },
    'age_first_funding_year': {
        'risk':    'Timing Risk — amplified by macro instability',
        'actions': [
            'Define 12-month milestones only — long-term planning unreliable in Lebanon',
            'Track 3 core metrics weekly: revenue, users, burn rate',
            'Document pivot criteria in advance to avoid reactive pivoting',
            'Attend iPark pitch clinics (8+/year) to sharpen market positioning',
        ]
    },
    'is_top500': {
        'risk':    'Ecosystem Risk — amplified by weakened local accelerator network',
        'actions': [
            'Apply to iPark BDD incubation program — strongest local network remaining',
            'Consider soft-landing to Cyprus via iPark Mediterraneo program',
            'Apply to EU Horizon grants — Lebanon still eligible',
            'Join regional accelerators (Flat6Labs, Wamda) for ecosystem access',
        ]
    },
    'funding_rounds': {
        'risk':    'Funding Risk — amplified by VC collapse and no pre-seed funds',
        'actions': [
            'Target diaspora investors via iPark Global Bridge Program',
            'Apply to EU Horizon grants — non-dilutive capital option',
            'Consider revenue-based financing to avoid equity dilution',
            'Set up international payment account (Stripe Atlas, Wise Business)',
        ]
    },
    'reached_series_b': {
        'risk':    'Execution Risk — amplified by infrastructure failure',
        'actions': [
            'Use cloud infrastructure (AWS/GCP) — avoid physical server dependency',
            'Build operational resilience plan for power and connectivity outages',
            'Establish international banking early — Lebanese banks unreliable',
            'Consider Cyprus entity via iPark Mediterraneo for international operations',
        ]
    },
}

# ── Dataset medians (for personal risk calculation) ───────────────────
MEDIANS = {
    'relationships':          df['relationships'].median(),
    'milestones':             df['milestones'].median(),
    'funding_rounds':         df['funding_rounds'].median(),
    'is_top500':              0.5,
    'reached_series_b':       0.5,
    'age_first_funding_year': df['age_first_funding_year'].median(),
}

# ── Global feature importance from RF (averaged RF+XGB as in notebook) ─
@st.cache_data
def compute_global_adjusted_risks():
    """
    Replicates the notebook's adjusted_df:
    GlobalImportance = average of RF + XGB feature importances for the 6 Lebanese risk features
    AdjustedRisk = GlobalImportance × FinalWeight
    """
    rf_imp  = dict(zip(FEATURES, clf.feature_importances_))
    # We only have RF saved; notebook averaged RF+XGB but RF is the deployed model
    # Use RF importances as global importance (consistent with saved model)
    rows = {}
    for feat, info in LEBANON_RISKS.items():
        global_imp    = rf_imp.get(feat, 0)
        final_weight  = info['final_weight']
        adjusted      = global_imp * final_weight
        rows[feat] = {
            'Global Risk':   round(global_imp,  4),
            'Final Weight':  round(final_weight, 2),
            'Adjusted Risk': round(adjusted,     4),
            'iPark Reason':  info['iPark_reason'],
        }
    return pd.DataFrame(rows).T.sort_values('Adjusted Risk', ascending=False)

adjusted_df = compute_global_adjusted_risks()

# ── Sidebar inputs ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 Startup Profile")
    st.markdown("---")
    sname = st.text_input("Startup name", "My Startup")
    st.markdown("### Funding")
    fr    = st.slider("Funding rounds completed", 0, 10, 1)
    hvc   = st.selectbox("VC backing?",    ["No", "Yes"])
    hang  = st.selectbox("Angel backing?", ["No", "Yes"])
    hra   = st.selectbox("Series A?",      ["No", "Yes"])
    hrb   = st.selectbox("Series B?",      ["No", "Yes"])
    hrc   = st.selectbox("Series C?",      ["No", "Yes"])
    hrd   = st.selectbox("Series D?",      ["No", "Yes"])
    st.markdown("### Team & Network")
    rels  = st.slider("Professional connections", 0, 30, 3)
    top500 = st.selectbox("In top accelerator network?", ["No", "Yes"])
    st.markdown("### Product & Timing")
    ms    = st.slider("Milestones hit", 0, 8, 1)
    aff   = st.slider("Years from founding to first funding", 0.0, 10.0, 1.0, 0.5)
    alf   = st.slider("Years from founding to last funding",  0.0, 15.0, 2.0, 0.5)

# ── Compute ───────────────────────────────────────────────────────────
HVC  = 1 if hvc  == "Yes" else 0
HANG = 1 if hang == "Yes" else 0
HRA  = 1 if hra  == "Yes" else 0
HRB  = 1 if hrb  == "Yes" else 0
HRC  = 1 if hrc  == "Yes" else 0
HRD  = 1 if hrd  == "Yes" else 0
IS500 = 1 if top500 == "Yes" else 0
RSB  = int(HRB or HRC)

# Step 1 — Baseline ML prediction (exactly as in notebook)
feat_vec = pd.DataFrame([[
    fr, HVC, HANG, HRA, HRB, HRC, HRD,
    ms, IS500, RSB, rels, aff, alf
]], columns=FEATURES)

baseline = clf.predict_proba(feat_vec)[0][1] * 100

# Step 2 — Personal risk ranking (exactly as in notebook dashboard cell)
# personal = adjusted_df.loc[feat, 'Adjusted Risk'] * (1 + gap)
# gap = max(0, median - value) / (median + 1e-9)  — below median = higher risk
startup_values = {
    'relationships':          rels,
    'milestones':             ms,
    'funding_rounds':         fr,
    'is_top500':              IS500,
    'reached_series_b':       RSB,
    'age_first_funding_year': aff,
}

startup_risks = {}
for feat, info in LEBANON_RISKS.items():
    val      = startup_values[feat]
    med      = MEDIANS[feat]
    gap      = max(0, med - val) / (med + 1e-9)
    personal = float(adjusted_df.loc[feat, 'Adjusted Risk']) * (1 + gap)
    startup_risks[feat] = round(personal, 4)

startup_df = pd.DataFrame.from_dict(
    startup_risks, orient='index', columns=['Personal Risk']
).sort_values('Personal Risk', ascending=False)

# Step 3 — Risk level based on baseline (as in notebook)
risk_level = ('CRITICAL' if baseline < 40 else
              'HIGH'     if baseline < 55 else
              'MODERATE' if baseline < 70 else 'GOOD')

rc  = {'GOOD': '#059669', 'MODERATE': '#d97706', 'HIGH': '#dc2626', 'CRITICAL': '#7c3aed'}[risk_level]
rbg = {'GOOD': 'rgba(5,150,105,0.08)', 'MODERATE': 'rgba(217,119,6,0.08)',
       'HIGH': 'rgba(220,38,38,0.08)', 'CRITICAL': 'rgba(124,58,237,0.08)'}[risk_level]

top3 = list(startup_df.head(3).index)
maxr = startup_df['Personal Risk'].max()

# ── ABOUT ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-card">
    <div class="about-icon">💡</div>
    <div class="about-title">About the Viability Engine</div>
    <div class="about-text">
        This decision-support tool uses machine learning trained on 923 real startup outcomes
        to predict baseline viability, then applies a Lebanese risk amplification layer grounded
        in iPark's expert research (Haidar &amp; Nohra, 2024) and peer-reviewed literature.
        The model achieves 80% AUC on held-out test data and confirms 6 of iPark's
        12 globally-identified failure reasons through data alone.
        Risk level is based on the global ML baseline. The Lebanese layer re-ranks which
        failure signals are most amplified by Lebanon's specific conditions.
    </div>
    <div class="about-grid">
        <div class="about-item">
            <div class="about-item-label">Data Source</div>
            <div class="about-item-val">923 real startup outcomes · Verified acquisition and closure events · Crunchbase</div>
        </div>
        <div class="about-item">
            <div class="about-item-label">ML Model</div>
            <div class="about-item-val">Random Forest · 80% AUC · 5-fold cross-validated · 13 features</div>
        </div>
        <div class="about-item">
            <div class="about-item-label">Lebanese Risk Layer</div>
            <div class="about-item-val">GlobalImportance × FinalWeight · FinalWeight = (iPark weight + Literature weight) / 2</div>
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
  <span class="hero-badge" style="background:{rbg};color:{rc};border:1px solid {rc}33">{risk_level}</span>
</div>""", unsafe_allow_html=True)

# ── METRICS ───────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="metric" style="--a:#6b1a2a"><div class="metric-label">Baseline Viability</div><div class="metric-val" style="color:#6b1a2a">{baseline:.1f}%</div><div class="metric-desc">Global ML · Random Forest · AUC 80%</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric" style="--a:{rc}"><div class="metric-label">Lebanon Risk Level</div><div class="metric-val" style="color:{rc}">{risk_level}</div><div class="metric-desc">Based on baseline vs global survival thresholds</div></div>', unsafe_allow_html=True)
with c3:
    top_risk_feat  = top3[0]
    top_risk_score = float(startup_df.loc[top_risk_feat, 'Personal Risk'])
    st.markdown(f'<div class="metric" style="--a:{IPARK_COLORS[top_risk_feat]}"><div class="metric-label">Highest Lebanese Risk</div><div class="metric-val" style="color:{IPARK_COLORS[top_risk_feat]}">{FEATURE_LABELS[top_risk_feat]}</div><div class="metric-desc">{IPARK_REASONS[top_risk_feat]} · score {top_risk_score:.3f}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── MIDDLE ────────────────────────────────────────────────────────────
left, right = st.columns([1.4, 1])

with left:
    st.markdown('<div class="sec-title">Personal Risk Ranking — Lebanon Amplification</div>', unsafe_allow_html=True)
    st.caption("Adjusted Risk = Global Feature Importance × Lebanese Weight × Personal Gap factor")
    for feat in startup_df.index:
        rv   = float(startup_df.loc[feat, 'Personal Risk'])
        pct  = (rv / maxr * 100) if maxr > 0 else 0
        col  = IPARK_COLORS[feat]
        lbl  = FEATURE_LABELS.get(feat, feat)
        reason = IPARK_REASONS[feat]
        global_risk = float(adjusted_df.loc[feat, 'Adjusted Risk'])
        fw   = float(adjusted_df.loc[feat, 'Final Weight'])
        st.markdown(f"""
        <div class="rbar">
          <div class="rbar-head">
            <span class="rbar-label">{lbl} <span style="font-size:10px;color:#bbb;font-weight:400">· {reason}</span></span>
            <span class="rbar-val">{rv:.3f} ({round(fw,2)}×)</span>
          </div>
          <div class="rbar-track"><div class="rbar-fill" style="width:{pct}%;background:{col}"></div></div>
        </div>""", unsafe_allow_html=True)

with right:
    # Strengths = features where you are AT or ABOVE the dataset median
    # Gaps = features where you are BELOW the dataset median
    strengths = []
    gaps_l    = []
    for f in startup_df.index:
        val = startup_values[f]
        med = MEDIANS[f]
        if val >= med:
            strengths.append(f)
        else:
            gaps_l.append(f)

    st.markdown('<div class="sec-title">Strengths</div>', unsafe_allow_html=True)
    if strengths:
        tags = "".join([f'<span class="tg tg-g">✓ {FEATURE_LABELS.get(f,f)}</span>' for f in strengths])
        st.markdown(f'<div class="tag-row">{tags}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="font-size:12px;color:#777">No strong signals detected</span>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Gap Alerts</div>', unsafe_allow_html=True)
    if gaps_l:
        tags = "".join([f'<span class="tg tg-r">△ {FEATURE_LABELS.get(f,f)}</span>' for f in gaps_l])
        st.markdown(f'<div class="tag-row">{tags}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="font-size:12px;color:#777">No critical gaps detected</span>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Viability Score</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="vbar-row">
      <div class="vbar-head"><span>Baseline (Global ML)</span><span style="color:#6b1a2a;font-weight:600">{baseline:.1f}%</span></div>
      <div class="vbar-track"><div class="vbar-fill" style="width:{baseline}%;background:#6b1a2a"></div></div>
    </div>
    <div style="font-size:10px;color:#777;margin-top:6px">
      GOOD ≥70% · MODERATE 55–70% · HIGH 40–55% · CRITICAL &lt;40%
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── RECOMMENDATIONS ───────────────────────────────────────────────────
st.markdown('<div class="sec-title">Top 3 Recommendations — Your Personal Lebanese Risk Profile</div>', unsafe_allow_html=True)
st.caption("Ranked by your personal adjusted risk · Linked to iPark Lebanon programs")

rc1, rc2, rc3 = st.columns(3)
for i, (feat, col) in enumerate(zip(top3, [rc1, rc2, rc3]), 1):
    rec   = RECOMMENDATIONS[feat]
    info  = LEBANON_RISKS[feat]
    score = float(startup_df.loc[feat, 'Personal Risk'])
    fw    = info['final_weight']
    color = IPARK_COLORS[feat]
    acts  = "".join([f'<div class="rec-act">{a}</div>' for a in rec['actions']])
    with col:
        st.markdown(f"""
        <div class="rec" style="--c:{color}">
          <div class="rec-num">Priority #{i} · Personal Risk Score {score:.3f}</div>
          <div class="rec-title" style="color:{color}">{FEATURE_LABELS[feat]}</div>
          <div class="rec-sub">{info['iPark_reason']}</div>
          {acts}
        </div>""", unsafe_allow_html=True)

# ── METHODOLOGY NOTE ──────────────────────────────────────────────────
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
with st.expander("Methodology — How the risk ranking works"):
    st.markdown("""
**Step 1 — Global ML Baseline**  
A Random Forest model trained on 923 Crunchbase startups predicts your acquisition probability.
Risk level thresholds: GOOD ≥70% · MODERATE 55–70% · HIGH 40–55% · CRITICAL <40%

**Step 2 — Lebanese Risk Amplification**  
Each of the 6 confirmed failure signals gets a Lebanese weight derived from two independent sources:
- *iPark priority weight* — from Hani Haidar & Maria Nohra's Lebanon failure taxonomy (position in their ranked list of 11 Lebanon-specific failure reasons)
- *Literature weight* — from World Bank, KAS/Arabnet, AGBI, HRW, Information International
- `FinalWeight = (iPark weight + Literature weight) / 2`

**Step 3 — Global Adjusted Risk**  
`AdjustedRisk = GlobalFeatureImportance × FinalWeight`  
This re-ranks which failure signals matter most in Lebanon — it does not simply amplify everything equally.

**Step 4 — Personal Risk Ranking**  
`PersonalRisk = AdjustedRisk × (1 + gap)`  
where `gap = max(0, median − yourValue) / median` — being below the dataset median increases your personal exposure to that failure signal.

**Key finding:**  
Lebanon re-ranks, not just amplifies. `relationships` stays #1 but becomes more dominant. `milestones` jumps to #2 because validating demand is harder when purchasing power has collapsed. `age_first_funding_year` drops to #3.

**Reference:** Haidar, H. & Nohra, M. (2024). *Why Startups Fail — Lebanon Version*. iPark, AUB Innovation Park.
    """)

# ── FOOTER ────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  iPark — Talal &amp; Madiha Zein AUB Innovation Park &nbsp;·&nbsp;
  ML Model: Random Forest · AUC 80% · 923 Crunchbase startups &nbsp;·&nbsp;
  Lebanese Risk Layer: Haidar &amp; Nohra (2024) + Literature Review
</div>""", unsafe_allow_html=True)
