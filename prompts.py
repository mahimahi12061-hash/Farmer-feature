import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PERSONA = """You are AgroMind AI, an expert agricultural advisory system combining
agronomy, plant pathology, soil science, and precision irrigation.
You give specific, actionable advice based on the farmer's actual field conditions."""

JSON_RULE = "\n\nRespond ONLY with valid JSON. No markdown, no backticks, no extra text."


def crop_health_prompt(ctx):
    return f"""{PERSONA}

{ctx}

Analyze crop health and return EXACTLY this JSON:
{{
  "overall_health_score": <integer 0-100>,
  "health_status": "<Excellent|Good|Fair|Poor|Critical>",
  "disease_risk_level": "<Low|Medium|High|Very High>",
  "water_stress_level": "<None|Mild|Moderate|Severe>",
  "nutrient_status": "<Deficient|Adequate|Optimal|Excessive>",
  "key_risks": ["<risk1>", "<risk2>", "<risk3>"],
  "positive_indicators": ["<indicator1>", "<indicator2>"],
  "immediate_actions": ["<action1>", "<action2>", "<action3>"],
  "summary": "<2 sentence summary>"
}}{JSON_RULE}"""


def disease_prevention_prompt(ctx):
    return f"""{PERSONA}

{ctx}

Generate a disease prevention plan as EXACTLY this JSON:
{{
  "risk_summary": "<2 sentence summary>",
  "current_threats": [
    {{"disease": "<name>", "risk": "<Low|Medium|High>", "cause": "<cause>", "symptoms_to_watch": "<symptoms>"}}
  ],
  "preventive_treatments": [
    {{"treatment": "<name>", "type": "<Biological|Chemical|Cultural>", "timing": "<when>", "dosage": "<rate>", "notes": "<tip>"}}
  ],
  "cultural_practices": ["<practice1>", "<practice2>", "<practice3>"],
  "monitoring_schedule": "<recommendation>"
}}{JSON_RULE}"""


def irrigation_prompt(ctx):
    return f"""{PERSONA}

{ctx}

Create an irrigation schedule as EXACTLY this JSON:
{{
  "advisory": "<2 sentence advisory>",
  "water_requirement_mm_per_day": <number>,
  "current_deficit_mm": <number>,
  "irrigation_needed": <true|false>,
  "next_irrigation_date": "<Today|Tomorrow|Day name>",
  "irrigation_duration_minutes": <integer>,
  "method_recommendation": "<Drip|Sprinkler|Flood|Furrow>",
  "weekly_schedule": [
    {{"day": "Mon", "action": "<Irrigate X mm | Skip | Monitor>", "reason": "<reason>"}},
    {{"day": "Tue", "action": "<action>", "reason": "<reason>"}},
    {{"day": "Wed", "action": "<action>", "reason": "<reason>"}},
    {{"day": "Thu", "action": "<action>", "reason": "<reason>"}},
    {{"day": "Fri", "action": "<action>", "reason": "<reason>"}},
    {{"day": "Sat", "action": "<action>", "reason": "<reason>"}},
    {{"day": "Sun", "action": "<action>", "reason": "<reason>"}}
  ],
  "water_saving_tips": ["<tip1>", "<tip2>", "<tip3>"]
}}{JSON_RULE}"""


def fertilizer_prompt(ctx):
    return f"""{PERSONA}

{ctx}

Create a fertilizer plan as EXACTLY this JSON:
{{
  "advisory": "<2 sentence advisory>",
  "npk_status": {{"N": "<Low|Adequate|Optimal|Excessive>", "P": "<Low|Adequate|Optimal|Excessive>", "K": "<Low|Adequate|Optimal|Excessive>"}},
  "deficiency_symptoms": ["<symptom>"],
  "recommended_fertilizers": [
    {{"fertilizer": "<name>", "npk_ratio": "<ratio>", "quantity_kg_per_acre": <number>, "timing": "<when>", "method": "<how>"}}
  ],
  "micronutrients_needed": ["<nutrient>"],
  "organic_amendments": ["<amendment>"],
  "next_application_date": "<recommendation>",
  "soil_health_tips": ["<tip1>", "<tip2>"]
}}{JSON_RULE}"""


def weather_advisory_prompt(ctx):
    return f"""{PERSONA}

{ctx}

Write a weather-based crop advisory covering:
1. Current conditions impact on the crop
2. Best timing for field operations
3. Weather-related risks to watch
4. Protective measures recommended
5. 7-day outlook and preparation tips

Write in clear practical paragraphs a farmer can act on directly."""


def chat_advisor_prompt(ctx, history, question):
    return f"""{PERSONA}

Farm Context:
{ctx}

Recent Conversation:
{history}

Farmer's Question: {question}

Give practical, specific advice for their crop and conditions. Under 280 words."""