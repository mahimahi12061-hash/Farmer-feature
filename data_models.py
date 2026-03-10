import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataclasses import dataclass, asdict


@dataclass
class FarmEnvironment:
    crop: str
    growth_stage: str
    region: str
    farm_size: float
    temperature: float
    humidity: float
    soil_moisture: float
    soil_ph: float
    rainfall_7d: float
    wind_speed: float
    sunlight_hours: float
    pest_observations: str
    last_fertilizer: str

    def to_context_string(self) -> str:
        return f"""
=== Farm Environmental Data ===
Crop            : {self.crop}
Growth Stage    : {self.growth_stage}
Region          : {self.region}
Farm Size       : {self.farm_size} acres
Temperature     : {self.temperature} C
Humidity        : {self.humidity}%
Soil Moisture   : {self.soil_moisture}%
Soil pH         : {self.soil_ph}
Rainfall (7d)   : {self.rainfall_7d} mm
Wind Speed      : {self.wind_speed} km/h
Sunlight        : {self.sunlight_hours} hrs/day
Pest/Disease    : {self.pest_observations}
Last Fertilizer : {self.last_fertilizer}
"""


@dataclass
class CropHealthResult:
    overall_health_score: int
    health_status: str
    disease_risk_level: str
    water_stress_level: str
    nutrient_status: str
    key_risks: list
    positive_indicators: list
    immediate_actions: list
    summary: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            overall_health_score=int(d.get("overall_health_score", 70)),
            health_status=str(d.get("health_status", "Good")),
            disease_risk_level=str(d.get("disease_risk_level", "Medium")),
            water_stress_level=str(d.get("water_stress_level", "Mild")),
            nutrient_status=str(d.get("nutrient_status", "Adequate")),
            key_risks=d.get("key_risks", []),
            positive_indicators=d.get("positive_indicators", []),
            immediate_actions=d.get("immediate_actions", []),
            summary=str(d.get("summary", "")),
        )


@dataclass
class DiseasePreventionResult:
    current_threats: list
    preventive_treatments: list
    cultural_practices: list
    monitoring_schedule: str
    risk_summary: str


@dataclass
class IrrigationResult:
    water_requirement_mm_per_day: float
    current_deficit_mm: float
    irrigation_needed: bool
    next_irrigation_date: str
    irrigation_duration_minutes: int
    method_recommendation: str
    weekly_schedule: list
    water_saving_tips: list
    advisory: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            water_requirement_mm_per_day=float(d.get("water_requirement_mm_per_day", 0)),
            current_deficit_mm=float(d.get("current_deficit_mm", 0)),
            irrigation_needed=bool(d.get("irrigation_needed", False)),
            next_irrigation_date=str(d.get("next_irrigation_date", "TBD")),
            irrigation_duration_minutes=int(d.get("irrigation_duration_minutes", 0)),
            method_recommendation=str(d.get("method_recommendation", "")),
            weekly_schedule=d.get("weekly_schedule", []),
            water_saving_tips=d.get("water_saving_tips", []),
            advisory=str(d.get("advisory", "")),
        )


@dataclass
class FertilizerResult:
    npk_status: dict
    deficiency_symptoms: list
    recommended_fertilizers: list
    micronutrients_needed: list
    organic_amendments: list
    next_application_date: str
    soil_health_tips: list
    advisory: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            npk_status=d.get("npk_status", {}),
            deficiency_symptoms=d.get("deficiency_symptoms", []),
            recommended_fertilizers=d.get("recommended_fertilizers", []),
            micronutrients_needed=d.get("micronutrients_needed", []),
            organic_amendments=d.get("organic_amendments", []),
            next_application_date=str(d.get("next_application_date", "")),
            soil_health_tips=d.get("soil_health_tips", []),
            advisory=str(d.get("advisory", "")),
        )