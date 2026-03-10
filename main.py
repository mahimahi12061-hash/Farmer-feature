import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import datetime
from config import APP_NAME, APP_TAGLINE, APP_VERSION, init_model
from data_models import FarmEnvironment
from health_engine import AdvisoryEngine
from app import inject_css, render_sidebar, render_hero
from app import tab_crop_health, tab_disease, tab_irrigation, tab_fertilizer, tab_weather, tab_chat

st.set_page_config(page_title="AgroMind AI", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

inject_css()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

api_key, env_data = render_sidebar()
render_hero()

if not api_key:
    st.markdown('<div class="awarn"><strong>👆 Enter your Gemini API Key in the sidebar to begin.</strong></div>', unsafe_allow_html=True)
    st.stop()

try:
    client = init_model(api_key)
    engine = AdvisoryEngine(client)
except Exception as e:
    st.error(f"❌ Could not initialise Gemini: {e}")
    st.stop()

t1,t2,t3,t4,t5,t6 = st.tabs(["🌿 Crop Health","🦠 Disease Prevention","💧 Irrigation","🧪 Fertilizer","🌤️ Weather Advisory","💬 AI Field Advisor"])

with t1: tab_crop_health(engine, env_data)
with t2: tab_disease(engine, env_data)
with t3: tab_irrigation(engine, env_data)
with t4: tab_fertilizer(engine, env_data)
with t5: tab_weather(engine, env_data)
with t6: tab_chat(engine, env_data)

st.markdown("---")
st.markdown(f'<div style="text-align:center;font-size:.75rem;color:#999;padding:1rem 0">{APP_NAME} v{APP_VERSION} · {APP_TAGLINE} · Powered by Gemini 2.0 Flash · {datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)