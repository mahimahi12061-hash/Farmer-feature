# 🌾 AgroMind AI — LLM Agricultural Advisory System

An AI-powered advisory system that uses **Google Gemini 1.5 Flash** to provide crop management, disease prevention, irrigation, and fertilizer recommendations based on environmental conditions.

## Features

- 🌿 **Crop Health Analysis** — AI health scoring (0–100), risk identification, immediate actions
- 🦠 **Disease Prevention** — Pathogen threat detection, IPM treatment plans, cultural practices
- 💧 **Smart Irrigation** — Water deficit calculation, 7-day precision irrigation schedules
- 🧪 **Fertilizer & Nutrition** — NPK status analysis, fertilizer recommendations with dosage
- 🌤️ **Weather Advisory** — Agrometeorological insights and field operation timing
- 💬 **AI Field Advisor** — Context-aware conversational agronomist chatbot

## Tech Stack

- Python 3.10+
- Streamlit
- Google Gemini API (`google-generativeai`)
- Prompt Engineering (structured JSON + narrative prompts)

## Project Structure

```
agromind/
├── main.py           # Streamlit entry point — orchestrates all tabs
├── app.py            # UI components: CSS, sidebar, hero, tab renderers
├── config.py         # App config, constants, model initialisation
├── data_models.py    # Dataclasses for farm environment & results
├── health_engine.py  # Core LLM inference engine (all advisory modules)
├── prompts.py        # All prompt templates
├── requirements.txt
└── README.md
```

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run main.py
```

### 3. Enter your Gemini API Key
- Get your free key at: https://aistudio.google.com/app/apikey
- Enter it in the sidebar when the app opens

## Architecture

```
Sidebar Inputs (env data)
        │
        ▼
FarmEnvironment (data_models.py)
        │
        ▼
AdvisoryEngine (health_engine.py)
        │ ← prompts.py (prompt templates)
        ▼
Google Gemini 1.5 Flash API
        │
        ▼
Parsed Results → Streamlit UI (app.py / main.py)
```

## No External APIs Required

- ✅ Only **Gemini API Key** needed
- ✅ No weather APIs, sensor APIs, or databases
- ✅ All intelligence from LLM transformer reasoning