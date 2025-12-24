"""
API routes for race-related endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import logging

from app.models.race import Race, RaceResults, RaceTelemetry, Standings
from app.services.fastf1_service import FastF1Service
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/races/{season}", response_model=List[Race])
async def get_races(season: int):
    """Get all races for a given season"""
    try:
        # Check cache first
        cache_key = f"races_{season}"
        cached_races = await cache_service.get(cache_key)
        
        if cached_races:
            return [Race(**race_data) for race_data in cached_races]
        
        # Fetch from FastF1
        races = await FastF1Service.get_races_for_season(season)
        
        if not races:
            raise HTTPException(status_code=404, detail=f"No races found for season {season}")
        
        # Cache the results
        races_data = [race.dict() for race in races]
        await cache_service.set(cache_key, races_data, ttl_hours=168)  # Cache for a week
        
        return races
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching races for season {season}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/race/{season}/{round}/results", response_model=RaceResults)
async def get_race_results(season: int, round: int):
    """Get race results for a specific race"""
    try:
        # Check cache first
        cache_key = f"race_results_{season}_{round}"
        cached_results = await cache_service.get(cache_key)
        
        if cached_results:
            return RaceResults(**cached_results)
        
        # Fetch from FastF1
        race_results = await FastF1Service.get_race_results(season, round)
        
        if not race_results:
            raise HTTPException(
                status_code=404, 
                detail=f"No results found for season {season}, round {round}"
            )
        
        # Cache the results
        await cache_service.set(cache_key, race_results.dict(), ttl_hours=24)
        
        return race_results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching race results for {season}/{round}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/race/{season}/{round}/telemetry", response_model=RaceTelemetry)
async def get_race_telemetry(season: int, round: int, lap: int = 1):
    """Get telemetry data for a specific race"""
    try:
        # Check cache first
        cache_key = f"race_telemetry_{season}_{round}_{lap}"
        cached_telemetry = await cache_service.get(cache_key)
        
        if cached_telemetry:
            return RaceTelemetry(**cached_telemetry)
        
        # Fetch from FastF1
        telemetry = await FastF1Service.get_race_telemetry(season, round, lap)
        
        if not telemetry:
            raise HTTPException(
                status_code=404, 
                detail=f"No telemetry found for season {season}, round {round}, lap {lap}"
            )
        
        # Cache the results
        await cache_service.set(cache_key, telemetry.dict(), ttl_hours=24)
        
        return telemetry
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching telemetry for {season}/{round}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/standings/{season}", response_model=Standings)
async def get_standings(season: int, round: Optional[int] = None):
    """Get championship standings for a season"""
    try:
        # Check cache first
        cache_key = f"standings_{season}_{round or 'latest'}"
        cached_standings = await cache_service.get(cache_key)
        
        if cached_standings:
            return Standings(**cached_standings)
        
        # Fetch from FastF1
        standings = await FastF1Service.get_standings(season, round)
        
        if not standings:
            raise HTTPException(
                status_code=404, 
                detail=f"No standings found for season {season}"
            )
        
        # Cache the results
        await cache_service.set(cache_key, standings.dict(), ttl_hours=24)
        
        return standings
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching standings for season {season}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
