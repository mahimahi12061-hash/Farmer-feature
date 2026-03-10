import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import os as _os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY   = _os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL     = "gemini-2.0-flash"
TEMPERATURE_JSON = 0.3
TEMPERATURE_TEXT = 0.65
TEMPERATURE_CHAT = 0.7

APP_NAME    = "AgroMind AI"
APP_VERSION = "1.0.0"
APP_TAGLINE = "LLM-Integrated Agricultural Advisory System"

CROP_LIST = [
    "Wheat", "Rice", "Maize/Corn", "Cotton", "Soybean",
    "Tomato", "Potato", "Sugarcane", "Sunflower",
    "Chickpea", "Groundnut", "Onion", "Chilli", "Mustard",
    "Barley", "Lentil", "Brinjal", "Okra", "Cabbage"
]

GROWTH_STAGES = [
    "Seedling (0-2 weeks)",
    "Vegetative (3-6 weeks)",
    "Flowering",
    "Fruiting / Grain Filling",
    "Maturity / Pre-Harvest"
]

def init_model(api_key: str = ""):
    key = api_key or GEMINI_API_KEY
    if not key:
        raise ValueError("No Gemini API key found.")
    return genai.Client(api_key=key)