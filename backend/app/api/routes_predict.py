"""
API routes for prediction endpoints
"""

from fastapi import APIRouter, HTTPException
import logging

from app.models.predict import PredictRequest, PredictResponse
from app.services.ml_service import MLService
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize ML service
ml_service = MLService()


@router.post("/predict", response_model=PredictResponse)
async def predict_race(request: PredictRequest):
    """Generate predictions for race or qualifying"""
    try:
        # Create cache key based on request parameters
        cache_key = f"predict_{request.season}_{request.round}_{request.session_type}_{request.weather_condition or 'default'}"
        
        # Check cache first (with shorter TTL for predictions)
        cached_prediction = await cache_service.get(cache_key)
        
        if cached_prediction:
            return PredictResponse(**cached_prediction)
        
        # Generate prediction based on session type
        if request.session_type.lower() == "qualifying":
            prediction = await ml_service.predict_qualifying(request)
        else:
            # For now, use the same prediction logic for race as qualifying
            # In a real implementation, you would have separate race prediction logic
            prediction = await ml_service.predict_qualifying(request)
        
        if not prediction.predictions:
            raise HTTPException(
                status_code=404, 
                detail="Could not generate predictions for the requested race"
            )
        
        # Cache the prediction with shorter TTL (1 hour)
        await cache_service.set(cache_key, prediction.dict(), ttl_hours=1)
        
        return prediction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
