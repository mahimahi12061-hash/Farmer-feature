import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json, re
from google.genai import types
from config import GEMINI_MODEL, TEMPERATURE_JSON, TEMPERATURE_TEXT, TEMPERATURE_CHAT
from data_models import FarmEnvironment, CropHealthResult, DiseasePreventionResult, IrrigationResult, FertilizerResult
from prompts import crop_health_prompt, disease_prevention_prompt, irrigation_prompt, fertilizer_prompt, weather_advisory_prompt, chat_advisor_prompt


def _json(client, prompt):
    r = client.models.generate_content(
        model=GEMINI_MODEL, contents=prompt,
        config=types.GenerateContentConfig(temperature=TEMPERATURE_JSON)
    )
    raw = re.sub(r"```json|```", "", r.text.strip()).strip()
    return json.loads(raw)


def _text(client, prompt, temp=TEMPERATURE_TEXT):
    r = client.models.generate_content(
        model=GEMINI_MODEL, contents=prompt,
        config=types.GenerateContentConfig(temperature=temp)
    )
    return r.text.strip()


class AdvisoryEngine:
    def __init__(self, client):
        self.client = client

    def analyze_crop_health(self, env: FarmEnvironment) -> CropHealthResult:
        return CropHealthResult.from_dict(_json(self.client, crop_health_prompt(env.to_context_string())))

    def get_disease_plan(self, env: FarmEnvironment) -> DiseasePreventionResult:
        d = _json(self.client, disease_prevention_prompt(env.to_context_string()))
        return DiseasePreventionResult(
            current_threats=d.get("current_threats", []),
            preventive_treatments=d.get("preventive_treatments", []),
            cultural_practices=d.get("cultural_practices", []),
            monitoring_schedule=d.get("monitoring_schedule", ""),
            risk_summary=d.get("risk_summary", ""),
        )

    def get_irrigation_plan(self, env: FarmEnvironment) -> IrrigationResult:
        return IrrigationResult.from_dict(_json(self.client, irrigation_prompt(env.to_context_string())))

    def get_fertilizer_plan(self, env: FarmEnvironment) -> FertilizerResult:
        return FertilizerResult.from_dict(_json(self.client, fertilizer_prompt(env.to_context_string())))

    def get_weather_advisory(self, env: FarmEnvironment) -> str:
        return _text(self.client, weather_advisory_prompt(env.to_context_string()))

    def chat(self, env: FarmEnvironment, history: list, user_message: str) -> str:
        hist = "\n".join([
            f"{'Farmer' if m['role']=='user' else 'AgroMind AI'}: {m['content']}"
            for m in history[-6:]
        ])
        return _text(self.client, chat_advisor_prompt(env.to_context_string(), hist, user_message), TEMPERATURE_CHAT)
