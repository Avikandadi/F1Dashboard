"""
FastF1 service for fetching F1 data
"""

import fastf1
from typing import List, Optional
import pandas as pd
from datetime import datetime
import logging
import os
from app.models.race import (
    Race, RaceResult, RaceResults, Driver, Constructor, 
    TelemetryPoint, DriverTelemetry, RaceTelemetry,
    DriverStanding, ConstructorStanding, Standings
)
from app.core.config import settings

# Configure FastF1 cache - create directory if it doesn't exist
os.makedirs(settings.fastf1_cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(settings.fastf1_cache_dir)

logger = logging.getLogger(__name__)


class FastF1Service:
    """Service for interacting with FastF1 library"""
    
    @staticmethod
    async def get_races_for_season(season: int) -> List[Race]:
        """Get all races for a given season"""
        try:
            schedule = fastf1.get_event_schedule(season)
            races = []
            
            for _, event in schedule.iterrows():
                if event['EventFormat'] == 'conventional':
                    race = Race(
                        season=season,
                        round=event['RoundNumber'],
                        race_name=event['EventName'],
                        circuit_name=event['Location'],
                        date=pd.to_datetime(event['EventDate']),
                        time=None,
                        url=None
                    )
                    races.append(race)
            
            return races
        except Exception as e:
            logger.error(f"Error fetching races for season {season}: {e}")
            return []
    
    @staticmethod
    async def get_race_results(season: int, round_number: int) -> Optional[RaceResults]:
        """Get race results for a specific race"""
        try:
            session = fastf1.get_session(season, round_number, 'R')
            session.load()
            
            # Get race info
            race = Race(
                season=season,
                round=round_number,
                race_name=session.event['EventName'],
                circuit_name=session.event['Location'],
                date=pd.to_datetime(session.event['EventDate']),
                time=None,
                url=None
            )
            
            # Get results
            results = session.results
            race_results = []
            
            for _, result in results.iterrows():
                driver = Driver(
                    driver_id=result['Abbreviation'],
                    first_name=result['FirstName'] if pd.notna(result['FirstName']) else "",
                    last_name=result['LastName'] if pd.notna(result['LastName']) else "",
                    code=result['Abbreviation'],
                    permanent_number=int(result['DriverNumber']) if pd.notna(result['DriverNumber']) else None,
                    team=result['TeamName'] if pd.notna(result['TeamName']) else None
                )
                
                constructor = Constructor(
                    constructor_id=result['TeamName'] if pd.notna(result['TeamName']) else "",
                    name=result['TeamName'] if pd.notna(result['TeamName']) else "",
                    nationality=""
                )
                
                race_result = RaceResult(
                    position=int(result['Position']) if pd.notna(result['Position']) else 0,
                    driver=driver,
                    constructor=constructor,
                    points=float(result['Points']) if pd.notna(result['Points']) else 0.0,
                    time=str(result['Time']) if pd.notna(result['Time']) else None,
                    status=result['Status'] if pd.notna(result['Status']) else "Unknown"
                )
                race_results.append(race_result)
            
            return RaceResults(race=race, results=race_results)
        
        except Exception as e:
            logger.error(f"Error fetching race results for {season}/{round_number}: {e}")
            return None
    
    @staticmethod
    async def get_race_telemetry(season: int, round_number: int, lap: int = 1) -> Optional[RaceTelemetry]:
        """Get telemetry data for a specific race and lap"""
        try:
            session = fastf1.get_session(season, round_number, 'R')
            session.load()
            
            # Get race info
            race = Race(
                season=season,
                round=round_number,
                race_name=session.event['EventName'],
                circuit_name=session.event['Location'],
                date=pd.to_datetime(session.event['EventDate']),
                time=None,
                url=None
            )
            
            # Get telemetry for fastest lap of each driver
            drivers_telemetry = []
            
            for driver_code in session.drivers:
                try:
                    driver_data = session.laps.pick_driver(driver_code).pick_fastest()
                    if driver_data.empty:
                        continue
                    
                    telemetry = driver_data.get_car_data()
                    
                    # Create driver object
                    driver_info = session.get_driver(driver_code)
                    driver = Driver(
                        driver_id=driver_code,
                        first_name=driver_info['FirstName'] if 'FirstName' in driver_info else "",
                        last_name=driver_info['LastName'] if 'LastName' in driver_info else "",
                        code=driver_code,
                        permanent_number=None,
                        team=driver_info.get('TeamName', None)
                    )
                    
                    # Process telemetry data (sample every 10th point to reduce data size)
                    telemetry_points = []
                    for i in range(0, len(telemetry), 10):
                        row = telemetry.iloc[i]
                        point = TelemetryPoint(
                            distance=float(row['Distance']) if pd.notna(row['Distance']) else 0.0,
                            speed=float(row['Speed']) if pd.notna(row['Speed']) else None,
                            throttle=float(row['Throttle']) if pd.notna(row['Throttle']) else None,
                            brake=bool(row['Brake']) if pd.notna(row['Brake']) else None,
                            gear=int(row['nGear']) if pd.notna(row['nGear']) else None,
                            rpm=float(row['RPM']) if pd.notna(row['RPM']) else None,
                            drs=bool(row['DRS']) if pd.notna(row['DRS']) else None
                        )
                        telemetry_points.append(point)
                    
                    driver_telemetry = DriverTelemetry(
                        driver=driver,
                        lap_number=lap,
                        lap_time=str(driver_data['LapTime'].iloc[0]) if not driver_data.empty else None,
                        telemetry=telemetry_points
                    )
                    drivers_telemetry.append(driver_telemetry)
                
                except Exception as e:
                    logger.warning(f"Could not get telemetry for driver {driver_code}: {e}")
                    continue
            
            return RaceTelemetry(race=race, drivers_telemetry=drivers_telemetry)
        
        except Exception as e:
            logger.error(f"Error fetching telemetry for {season}/{round_number}: {e}")
            return None
    
    @staticmethod
    async def get_standings(season: int, round_number: Optional[int] = None) -> Optional[Standings]:
        """Get championship standings"""
        try:
            # For now, return mock standings since FastF1 doesn't have direct standings API
            # In a real implementation, you would fetch this from another API or calculate it
            driver_standings = [
                DriverStanding(
                    position=1,
                    driver=Driver(
                        driver_id="VER",
                        first_name="Max",
                        last_name="Verstappen",
                        code="VER",
                        permanent_number=1,
                        team="Red Bull Racing"
                    ),
                    constructor=Constructor(
                        constructor_id="red_bull",
                        name="Red Bull Racing",
                        nationality="Austrian"
                    ),
                    points=400.0,
                    wins=10
                )
            ]
            
            constructor_standings = [
                ConstructorStanding(
                    position=1,
                    constructor=Constructor(
                        constructor_id="red_bull",
                        name="Red Bull Racing",
                        nationality="Austrian"
                    ),
                    points=650.0,
                    wins=15
                )
            ]
            
            return Standings(
                season=season,
                round=round_number or 22,
                driver_standings=driver_standings,
                constructor_standings=constructor_standings
            )
        
        except Exception as e:
            logger.error(f"Error fetching standings for {season}: {e}")
            return None
