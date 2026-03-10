import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from data_models import FarmEnvironment
from config import CROP_LIST, GROWTH_STAGES


# ── CSS ────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root{--moss:#1A3A1F;--leaf:#2D6A35;--sprout:#4CAF50;--sun:#F4C430;--soil:#2D1B0E;--mist:#E8F5E9;--fog:#F1F8E9;--ink:#1C1C1C;--paper:#FAFDF7;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background:var(--paper);color:var(--ink);}
section[data-testid="stSidebar"]{background:linear-gradient(175deg,var(--moss),var(--soil));border-right:3px solid var(--leaf);}
section[data-testid="stSidebar"] *{color:var(--mist) !important;}
section[data-testid="stSidebar"] label{color:var(--sun) !important;font-family:'Syne',sans-serif !important;font-size:.72rem !important;letter-spacing:.1em !important;text-transform:uppercase !important;}
.hero{background:linear-gradient(135deg,var(--moss),var(--leaf),#5CB85C);padding:2.5rem 3rem;border-radius:16px;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero::before{content:'🌾';font-size:9rem;position:absolute;right:2.5rem;top:50%;transform:translateY(-50%);opacity:.1;}
.hero-title{font-family:'Syne',sans-serif;font-size:2.8rem;font-weight:800;color:#fff;margin:0;line-height:1.1;}
.hero-sub{color:rgba(255,255,255,.72);font-size:1rem;margin-top:.4rem;}
.hero-badge{display:inline-block;background:var(--sun);color:var(--soil);padding:.2rem .9rem;border-radius:20px;font-size:.68rem;font-weight:700;font-family:'Syne',sans-serif;letter-spacing:.08em;text-transform:uppercase;margin-top:.8rem;}
.mcard{background:white;border:1.5px solid #DCF0DC;border-left:5px solid var(--sprout);border-radius:12px;padding:1.1rem 1.4rem;margin-bottom:.9rem;box-shadow:0 2px 12px rgba(45,106,53,.07);}
.mlabel{font-family:'Syne',sans-serif;font-size:.63rem;font-weight:700;color:var(--leaf);letter-spacing:.13em;text-transform:uppercase;margin-bottom:.3rem;}
.mvalue{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:var(--ink);line-height:1;}
.munit{font-size:.82rem;color:#888;font-weight:400;}
.stitle{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;color:var(--moss);border-bottom:2px solid var(--sprout);padding-bottom:.35rem;margin:1.2rem 0 1rem 0;}
.aibox{background:linear-gradient(135deg,#F0FAF0,#FAFFF6);border:1.5px solid #B8DFB8;border-left:5px solid var(--leaf);border-radius:12px;padding:1.4rem 1.8rem;margin:1rem 0;line-height:1.7;}
.aihead{font-family:'Syne',sans-serif;font-size:.7rem;font-weight:700;color:var(--leaf);letter-spacing:.1em;text-transform:uppercase;margin-bottom:.8rem;}
.acrit{background:#FFF3F3;border-left:5px solid #E53935;border-radius:8px;padding:.9rem 1.1rem;margin:.45rem 0;}
.awarn{background:#FFFDE7;border-left:5px solid var(--sun);border-radius:8px;padding:.9rem 1.1rem;margin:.45rem 0;}
.aok{background:var(--fog);border-left:5px solid var(--sprout);border-radius:8px;padding:.9rem 1.1rem;margin:.45rem 0;}
.pill{display:inline-block;padding:.18rem .7rem;border-radius:20px;font-size:.68rem;font-weight:700;font-family:'Syne',sans-serif;letter-spacing:.06em;}
.pg{background:#C8E6C9;color:#1B5E20;}
.py{background:#FFF9C4;color:#F57F17;}
.pr{background:#FFCDD2;color:#B71C1C;}
.pb{background:#E3F2FD;color:#0D47A1;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:var(--fog);border-radius:10px;padding:4px;}
.stTabs [data-baseweb="tab"]{font-family:'Syne',sans-serif;font-weight:600;font-size:.78rem;border-radius:8px;padding:.45rem 1.1rem;color:#4A2C17 !important;}
.stTabs [aria-selected="true"]{background:var(--leaf) !important;color:white !important;}
.stButton>button{background:linear-gradient(135deg,var(--leaf),var(--sprout));color:white;border:none;border-radius:8px;font-family:'Syne',sans-serif;font-weight:700;font-size:.83rem;padding:.55rem 1.4rem;box-shadow:0 3px 10px rgba(45,106,53,.28);}
.stButton>button:hover{transform:translateY(-1px);box-shadow:0 5px 16px rgba(45,106,53,.38);}
.stTextInput input,.stTextArea textarea{border:1.5px solid #C8E6C9 !important;border-radius:8px !important;}
.cu{background:#E8F5E9;border-radius:14px 14px 3px 14px;padding:.75rem 1.1rem;margin:.5rem 0;max-width:82%;margin-left:auto;font-size:.9rem;}
.ca{background:white;border:1.5px solid #C8E6C9;border-radius:14px 14px 14px 3px;padding:.75rem 1.1rem;margin:.5rem 0;max-width:90%;font-size:.9rem;box-shadow:0 2px 8px rgba(0,0,0,.05);}
.clabel{font-size:.63rem;font-weight:700;font-family:'Syne',sans-serif;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.25rem;}
#MainMenu,footer,header{visibility:hidden;}
</style>""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def _sec(t):
    st.markdown(f'<div class="stitle">{t}</div>', unsafe_allow_html=True)

def _aibox(header, body):
    st.markdown(f'<div class="aibox"><div class="aihead">🤖 {header}</div>{body}</div>', unsafe_allow_html=True)

def _card(label, value, unit="", pill="", pc="pg"):
    ph = f'<br><span class="pill {pc}">{pill}</span>' if pill else ""
    st.markdown(f'<div class="mcard"><div class="mlabel">{label}</div><div class="mvalue">{value}<span class="munit"> {unit}</span></div>{ph}</div>', unsafe_allow_html=True)

def _pc(s):
    s = str(s).lower()
    if s in ("high","very high","critical","severe","poor","deficient","low"): return "pr"
    if s in ("medium","fair","mild","moderate"): return "py"
    return "pg"


# ── Sidebar ────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🌱 AgroMind AI")
        st.markdown("---")
        api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste your key here...")
        st.markdown("---")
        st.markdown('<p style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:#A5D6A7;font-family:Syne,sans-serif;font-weight:700">Farm Config</p>', unsafe_allow_html=True)
        crop         = st.selectbox("Crop", CROP_LIST)
        growth_stage = st.selectbox("Growth Stage", GROWTH_STAGES)
        region       = st.text_input("Region", placeholder="e.g. Punjab, India")
        farm_size    = st.number_input("Farm Size (acres)", 0.5, 5000.0, 5.0, step=0.5)
        st.markdown("---")
        st.markdown('<p style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:#A5D6A7;font-family:Syne,sans-serif;font-weight:700">Environment</p>', unsafe_allow_html=True)
        temperature   = st.slider("Temperature (°C)", -5, 50, 28)
        humidity      = st.slider("Humidity (%)", 10, 100, 65)
        soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 45)
        soil_ph       = st.slider("Soil pH", 4.0, 9.0, 6.5, step=0.1)
        rainfall      = st.number_input("Rainfall last 7 days (mm)", 0, 500, 12)
        wind_speed    = st.number_input("Wind Speed (km/h)", 0, 120, 15)
        sunlight      = st.slider("Sunlight Hours/day", 0, 14, 8)
        st.markdown("---")
        st.markdown('<p style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:#A5D6A7;font-family:Syne,sans-serif;font-weight:700">Observations</p>', unsafe_allow_html=True)
        pest_obs        = st.text_input("Pest / Disease Seen", placeholder="e.g. aphids on leaves")
        last_fertilizer = st.text_input("Last Fertilizer Applied", placeholder="e.g. Urea 2 weeks ago")

    env = FarmEnvironment(
        crop=crop, growth_stage=growth_stage,
        region=region or "Not specified", farm_size=farm_size,
        temperature=temperature, humidity=humidity,
        soil_moisture=soil_moisture, soil_ph=soil_ph,
        rainfall_7d=rainfall, wind_speed=wind_speed,
        sunlight_hours=sunlight,
        pest_observations=pest_obs or "None observed",
        last_fertilizer=last_fertilizer or "Not specified",
    )
    return api_key, env


# ── Hero ───────────────────────────────────────────────────────────────────────
def render_hero():
    st.markdown("""
<div class="hero">
  <div class="hero-title">AgroMind AI</div>
  <div class="hero-sub">LLM-Integrated Agricultural Advisory System</div>
  <div class="hero-badge">Powered by Google Gemini 2.0 Flash</div>
</div>""", unsafe_allow_html=True)


# ── Tab 1: Crop Health ─────────────────────────────────────────────────────────
def tab_crop_health(engine, env):
    _sec("🌿 Crop Health Analysis")
    if st.button("Analyse Crop Health", key="btn_health"):
        with st.spinner("Analysing..."):
            try:
                r = engine.analyze_crop_health(env)
                score = r.overall_health_score
                pc = "pg" if score >= 70 else "py" if score >= 45 else "pr"
                c1,c2,c3,c4 = st.columns(4)
                with c1: _card("Health Score", score, "/100", r.health_status, pc)
                with c2: _card("Disease Risk", r.disease_risk_level, pc=_pc(r.disease_risk_level))
                with c3: _card("Water Stress", r.water_stress_level, pc=_pc(r.water_stress_level))
                with c4: _card("Nutrient Status", r.nutrient_status, pc=_pc(r.nutrient_status))
                _aibox("Analysis Summary", f"<p>{r.summary}</p>")
                cl, cr = st.columns(2)
                with cl:
                    _sec("⚠️ Key Risks")
                    for x in r.key_risks: st.markdown(f'<div class="awarn">⚡ {x}</div>', unsafe_allow_html=True)
                with cr:
                    _sec("✅ Positive Indicators")
                    for x in r.positive_indicators: st.markdown(f'<div class="aok">✅ {x}</div>', unsafe_allow_html=True)
                _sec("🎯 Immediate Actions")
                for i,a in enumerate(r.immediate_actions,1): st.markdown(f'<div class="aok"><strong>Action {i}:</strong> {a}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


# ── Tab 2: Disease ─────────────────────────────────────────────────────────────
def tab_disease(engine, env):
    _sec("🦠 Disease Prevention & Management")
    if st.button("Generate Disease Plan", key="btn_disease"):
        with st.spinner("Analysing..."):
            try:
                r = engine.get_disease_plan(env)
                _aibox("Disease Risk Summary", f"<p>{r.risk_summary}</p>")
                _sec("⚠️ Current Threats")
                for t in r.current_threats:
                    risk = t.get("risk","Low")
                    box = "acrit" if risk=="High" else "awarn" if risk=="Medium" else "aok"
                    pc2 = "pr" if risk=="High" else "py" if risk=="Medium" else "pg"
                    st.markdown(f'<div class="{box}"><strong>🦠 {t.get("disease","")}</strong> <span class="pill {pc2}">{risk} Risk</span><br><small><b>Cause:</b> {t.get("cause","")} | <b>Watch for:</b> {t.get("symptoms_to_watch","")}</small></div>', unsafe_allow_html=True)
                _sec("💊 Preventive Treatments")
                for tx in r.preventive_treatments:
                    st.markdown(f'<div class="mcard"><strong>{tx.get("treatment","")}</strong> <span class="pill pb">{tx.get("type","")}</span><br><small>⏰ {tx.get("timing","")} | 📦 {tx.get("dosage","")} | {tx.get("notes","")}</small></div>', unsafe_allow_html=True)
                cl,cr = st.columns(2)
                with cl:
                    _sec("🌾 Cultural Practices")
                    for p in r.cultural_practices: st.markdown(f"- {p}")
                with cr:
                    _sec("📅 Monitoring")
                    st.info(r.monitoring_schedule)
            except Exception as e:
                st.error(f"Error: {e}")


# ── Tab 3: Irrigation ──────────────────────────────────────────────────────────
def tab_irrigation(engine, env):
    _sec("💧 Smart Irrigation Management")
    if st.button("Generate Irrigation Schedule", key="btn_irr"):
        with st.spinner("Calculating..."):
            try:
                r = engine.get_irrigation_plan(env)
                c1,c2,c3,c4 = st.columns(4)
                with c1: _card("Daily Requirement", r.water_requirement_mm_per_day, "mm/day")
                with c2: _card("Current Deficit", r.current_deficit_mm, "mm")
                with c3: _card("Next Irrigation", r.next_irrigation_date)
                with c4: _card("Duration", r.irrigation_duration_minutes, "min")
                if r.irrigation_needed:
                    st.markdown('<div class="awarn">💧 <b>Irrigation Required</b></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="aok">✅ <b>No immediate irrigation needed</b></div>', unsafe_allow_html=True)
                _aibox("Irrigation Advisory", f"<p>{r.advisory}</p><p><b>Method:</b> {r.method_recommendation}</p>")
                _sec("📅 7-Day Schedule")
                cols = st.columns(7)
                for col, d in zip(cols, r.weekly_schedule):
                    a = d.get("action","")
                    bg = "#E8F5E9" if ("Skip" in a or "Monitor" in a) else "#FFF9C4"
                    with col:
                        st.markdown(f'<div style="background:{bg};border-radius:9px;padding:.75rem .4rem;text-align:center;border:1px solid #ddd"><div style="font-family:Syne,sans-serif;font-weight:700;font-size:.72rem;color:#555">{d.get("day","")}</div><div style="font-size:.78rem;font-weight:600;margin:.25rem 0">{a}</div><div style="font-size:.66rem;color:#777">{d.get("reason","")}</div></div>', unsafe_allow_html=True)
                _sec("💡 Water Saving Tips")
                for tip in r.water_saving_tips: st.markdown(f"💡 {tip}")
            except Exception as e:
                st.error(f"Error: {e}")


# ── Tab 4: Fertilizer ──────────────────────────────────────────────────────────
def tab_fertilizer(engine, env):
    _sec("🧪 Fertilizer & Nutrition Management")
    if st.button("Generate Fertilizer Plan", key="btn_fert"):
        with st.spinner("Analysing..."):
            try:
                r = engine.get_fertilizer_plan(env)
                npk = r.npk_status
                c1,c2,c3 = st.columns(3)
                for col,label,key in [(c1,"Nitrogen (N)","N"),(c2,"Phosphorus (P)","P"),(c3,"Potassium (K)","K")]:
                    s = npk.get(key,"Adequate")
                    with col: _card(label, s, pc=_pc(s))
                _aibox("Nutrition Advisory", f"<p>{r.advisory}</p>")
                _sec("🌿 Recommended Fertilizers")
                for f in r.recommended_fertilizers:
                    st.markdown(f'<div class="mcard"><strong>{f.get("fertilizer","")}</strong> <span class="pill pg">NPK {f.get("npk_ratio","")}</span><br><small>📦 <b>{f.get("quantity_kg_per_acre","")} kg/acre</b> | ⏰ {f.get("timing","")} | 🔧 {f.get("method","")}</small></div>', unsafe_allow_html=True)
                cl,cr = st.columns(2)
                with cl:
                    _sec("🔬 Micronutrients")
                    for m in r.micronutrients_needed: st.markdown(f"- {m}")
                with cr:
                    _sec("♻️ Organic Amendments")
                    for a in r.organic_amendments: st.markdown(f"- {a}")
                st.markdown(f"📅 **Next Application:** {r.next_application_date}")
            except Exception as e:
                st.error(f"Error: {e}")


# ── Tab 5: Weather ─────────────────────────────────────────────────────────────
def tab_weather(engine, env):
    _sec("🌤️ Weather Advisory")
    c1,c2,c3,c4 = st.columns(4)
    with c1: _card("Temperature", f"{env.temperature}°C")
    with c2: _card("Humidity", f"{env.humidity}%")
    with c3: _card("Rainfall 7d", f"{env.rainfall_7d} mm")
    with c4: _card("Wind Speed", f"{env.wind_speed} km/h")
    if st.button("Get Weather Advisory", key="btn_weather"):
        with st.spinner("Generating..."):
            try:
                adv = engine.get_weather_advisory(env)
                _aibox("Agrometeorological Advisory", adv.replace("\n","<br>"))
            except Exception as e:
                st.error(f"Error: {e}")


# ── Tab 6: Chat ────────────────────────────────────────────────────────────────
QUICK_QS = [
    "Best time to spray pesticides today?",
    "How to improve soil organic matter?",
    "Signs of overwatering vs underwatering?",
    "How to identify nutrient deficiency?",
    "Organic alternatives to chemical fertilizers?",
    "How to protect crop from heat stress?",
]

def tab_chat(engine, env):
    _sec("💬 AI Field Advisor — Ask Anything")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div style="text-align:right"><div class="clabel" style="color:#555;text-align:right">You</div><div class="cu">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div><div class="clabel" style="color:#2D6A35">🤖 AgroMind AI</div><div class="ca">{msg["content"]}</div></div>', unsafe_allow_html=True)

    st.markdown("**💡 Quick questions:**")
    qc = st.columns(3)
    for i, q in enumerate(QUICK_QS):
        with qc[i % 3]:
            if st.button(q, key=f"qq_{i}"):
                st.session_state["_pending"] = q

    user_input = st.text_input("Ask your question...", placeholder="e.g. My wheat leaves are yellowing — what's wrong?", key="chat_input")
    c1, c2, _ = st.columns([1,1,5])
    with c1: send = st.button("Send", key="send_btn")
    with c2:
        if st.button("Clear", key="clear_btn"):
            st.session_state.chat_history = []
            st.rerun()

    pending = st.session_state.pop("_pending", None)
    if pending:
        user_input = pending
        send = True

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            try:
                reply = engine.chat(env, st.session_state.chat_history, user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")