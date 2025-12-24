"""
Prediction-related Pydantic models
"""

from typing import List, Optional
from pydantic import BaseModel
from app.models.race import Driver


class PredictRequest(BaseModel):
    """Request model for predictions"""
    season: int
    round: int
    session_type: str = "qualifying"  # "qualifying" or "race"
    weather_condition: Optional[str] = None
    track_temperature: Optional[float] = None
    air_temperature: Optional[float] = None


class DriverPrediction(BaseModel):
    """Single driver prediction"""
    driver: Driver
    predicted_position: int
    confidence: float
    reasoning: Optional[str] = None


class PredictResponse(BaseModel):
    """Response model for predictions"""
    session_type: str
    race_name: str
    circuit_name: str
    predictions: List[DriverPrediction]
    model_info: dict
    generated_at: str
