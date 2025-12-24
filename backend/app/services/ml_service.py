"""
ML service for F1 predictions
"""

import pickle
import numpy as np
from datetime import datetime
from typing import List, Optional
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

from app.models.predict import PredictRequest, PredictResponse, DriverPrediction
from app.models.race import Driver, Constructor
from app.core.config import settings

logger = logging.getLogger(__name__)


class MLService:
    """Service for machine learning predictions"""
    
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.model_path = os.path.join(settings.model_path, "f1_prediction_model.joblib")
        self.encoders_path = os.path.join(settings.model_path, "label_encoders.joblib")
        
        # Create model directory if it doesn't exist
        os.makedirs(settings.model_path, exist_ok=True)
        
        # Load or create model
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a dummy one"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.encoders_path):
                self.model = joblib.load(self.model_path)
                self.label_encoders = joblib.load(self.encoders_path)
                logger.info("Loaded existing ML model")
            else:
                self._create_dummy_model()
                logger.info("Created dummy ML model")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a dummy model for demonstration purposes"""
        try:
            # Create dummy training data
            np.random.seed(42)
            n_samples = 1000
            
            # Features: driver_encoded, constructor_encoded, track_temp, air_temp, weather_encoded
            X = np.random.rand(n_samples, 5)
            
            # Target: finishing position (1-20)
            y = np.random.randint(1, 21, n_samples)
            
            # Create and train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X, y)
            
            # Create dummy label encoders
            self.label_encoders = {
                'driver': LabelEncoder(),
                'constructor': LabelEncoder(),
                'weather': LabelEncoder()
            }
            
            # Fit encoders with dummy data
            dummy_drivers = ['VER', 'HAM', 'LEC', 'SAI', 'RUS', 'NOR', 'PIA', 'ALO', 'STR', 'PER']
            dummy_constructors = ['Red Bull', 'Mercedes', 'Ferrari', 'McLaren', 'Aston Martin']
            dummy_weather = ['Dry', 'Wet', 'Intermediate']
            
            self.label_encoders['driver'].fit(dummy_drivers)
            self.label_encoders['constructor'].fit(dummy_constructors)
            self.label_encoders['weather'].fit(dummy_weather)
            
            # Save model and encoders
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.label_encoders, self.encoders_path)
            
        except Exception as e:
            logger.error(f"Error creating dummy model: {e}")
            # Fallback: simple random model
            self.model = None
            self.label_encoders = {}
    
    async def predict_qualifying(self, request: PredictRequest) -> PredictResponse:
        """Predict qualifying results"""
        try:
            # Mock drivers for demonstration
            mock_drivers = [
                Driver(driver_id="VER", first_name="Max", last_name="Verstappen", code="VER", permanent_number=1, team="Red Bull Racing"),
                Driver(driver_id="HAM", first_name="Lewis", last_name="Hamilton", code="HAM", permanent_number=44, team="Mercedes"),
                Driver(driver_id="LEC", first_name="Charles", last_name="Leclerc", code="LEC", permanent_number=16, team="Ferrari"),
                Driver(driver_id="SAI", first_name="Carlos", last_name="Sainz Jr", code="SAI", permanent_number=55, team="Ferrari"),
                Driver(driver_id="RUS", first_name="George", last_name="Russell", code="RUS", permanent_number=63, team="Mercedes"),
                Driver(driver_id="NOR", first_name="Lando", last_name="Norris", code="NOR", permanent_number=4, team="McLaren"),
                Driver(driver_id="PIA", first_name="Oscar", last_name="Piastri", code="PIA", permanent_number=81, team="McLaren"),
                Driver(driver_id="ALO", first_name="Fernando", last_name="Alonso", code="ALO", permanent_number=14, team="Aston Martin"),
                Driver(driver_id="STR", first_name="Lance", last_name="Stroll", code="STR", permanent_number=18, team="Aston Martin"),
                Driver(driver_id="PER", first_name="Sergio", last_name="Perez", code="PER", permanent_number=11, team="Red Bull Racing"),
            ]
            
            predictions = []
            
            if self.model is not None:
                # Use the actual model for predictions
                for i, driver in enumerate(mock_drivers):
                    # Create feature vector
                    features = self._create_feature_vector(driver, request)
                    
                    # Predict position
                    predicted_pos = self.model.predict([features])[0]
                    confidence = np.random.uniform(0.6, 0.95)  # Random confidence for demo
                    
                    prediction = DriverPrediction(
                        driver=driver,
                        predicted_position=int(predicted_pos),
                        confidence=confidence,
                        reasoning=f"Based on historical performance and current conditions"
                    )
                    predictions.append(prediction)
            else:
                # Fallback: random predictions
                positions = list(range(1, len(mock_drivers) + 1))
                np.random.shuffle(positions)
                
                for i, driver in enumerate(mock_drivers):
                    prediction = DriverPrediction(
                        driver=driver,
                        predicted_position=positions[i],
                        confidence=np.random.uniform(0.5, 0.8),
                        reasoning="Random prediction (model not available)"
                    )
                    predictions.append(prediction)
            
            # Sort by predicted position
            predictions.sort(key=lambda x: x.predicted_position)
            
            return PredictResponse(
                session_type=request.session_type,
                race_name=f"Race {request.round}",
                circuit_name="Mock Circuit",
                predictions=predictions,
                model_info={
                    "model_type": "Random Forest" if self.model else "Random",
                    "version": "1.0.0",
                    "features": ["driver", "constructor", "track_temp", "air_temp", "weather"]
                },
                generated_at=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            # Return empty prediction on error
            return PredictResponse(
                session_type=request.session_type,
                race_name="Unknown",
                circuit_name="Unknown",
                predictions=[],
                model_info={"error": str(e)},
                generated_at=datetime.now().isoformat()
            )
    
    def _create_feature_vector(self, driver: Driver, request: PredictRequest) -> List[float]:
        """Create feature vector for prediction"""
        features = []
        
        try:
            # Driver encoding
            if 'driver' in self.label_encoders:
                try:
                    driver_encoded = self.label_encoders['driver'].transform([driver.code])[0]
                except ValueError:
                    driver_encoded = 0  # Unknown driver
            else:
                driver_encoded = 0
            features.append(float(driver_encoded))
            
            # Constructor encoding
            if 'constructor' in self.label_encoders:
                try:
                    constructor_encoded = self.label_encoders['constructor'].transform([driver.team or "Unknown"])[0]
                except ValueError:
                    constructor_encoded = 0  # Unknown constructor
            else:
                constructor_encoded = 0
            features.append(float(constructor_encoded))
            
            # Track temperature
            features.append(float(request.track_temperature or 25.0))
            
            # Air temperature
            features.append(float(request.air_temperature or 20.0))
            
            # Weather encoding
            if 'weather' in self.label_encoders:
                try:
                    weather_encoded = self.label_encoders['weather'].transform([request.weather_condition or "Dry"])[0]
                except ValueError:
                    weather_encoded = 0  # Unknown weather
            else:
                weather_encoded = 0
            features.append(float(weather_encoded))
            
        except Exception as e:
            logger.error(f"Error creating feature vector: {e}")
            # Return default features
            features = [0.0, 0.0, 25.0, 20.0, 0.0]
        
        return features
