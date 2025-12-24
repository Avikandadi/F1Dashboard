"""
Test prediction endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict_qualifying():
    """Test the qualifying prediction endpoint"""
    request_data = {
        "season": 2024,
        "round": 1,
        "session_type": "qualifying",
        "weather_condition": "Dry",
        "track_temperature": 30.0,
        "air_temperature": 25.0
    }
    
    response = client.post("/api/predict", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "session_type" in data
    assert "predictions" in data
    assert "model_info" in data
    assert data["session_type"] == "qualifying"
    
    # Check predictions structure
    predictions = data["predictions"]
    assert len(predictions) > 0
    
    for prediction in predictions:
        assert "driver" in prediction
        assert "predicted_position" in prediction
        assert "confidence" in prediction
        assert isinstance(prediction["predicted_position"], int)
        assert 0.0 <= prediction["confidence"] <= 1.0


def test_predict_race():
    """Test the race prediction endpoint"""
    request_data = {
        "season": 2024,
        "round": 1,
        "session_type": "race"
    }
    
    response = client.post("/api/predict", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["session_type"] == "race"
    assert "predictions" in data
