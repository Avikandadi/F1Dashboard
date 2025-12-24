"""
Race-related Pydantic models
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Driver(BaseModel):
    """Driver model"""
    driver_id: str
    first_name: str
    last_name: str
    code: str
    permanent_number: Optional[int] = None
    team: Optional[str] = None


class Constructor(BaseModel):
    """Constructor/Team model"""
    constructor_id: str
    name: str
    nationality: str


class RaceResult(BaseModel):
    """Single race result model"""
    position: int
    driver: Driver
    constructor: Constructor
    points: float
    time: Optional[str] = None
    status: str
    fastest_lap: Optional[str] = None
    fastest_lap_rank: Optional[int] = None


class Race(BaseModel):
    """Race model"""
    season: int
    round: int
    race_name: str
    circuit_name: str
    date: datetime
    time: Optional[str] = None
    url: Optional[str] = None


class RaceResults(BaseModel):
    """Complete race results model"""
    race: Race
    results: List[RaceResult]


class TelemetryPoint(BaseModel):
    """Single telemetry data point"""
    distance: float
    speed: Optional[float] = None
    throttle: Optional[float] = None
    brake: Optional[float] = None
    gear: Optional[int] = None
    rpm: Optional[float] = None
    drs: Optional[bool] = None


class DriverTelemetry(BaseModel):
    """Driver telemetry for a lap"""
    driver: Driver
    lap_number: int
    lap_time: Optional[str] = None
    telemetry: List[TelemetryPoint]


class RaceTelemetry(BaseModel):
    """Complete race telemetry model"""
    race: Race
    drivers_telemetry: List[DriverTelemetry]


class DriverStanding(BaseModel):
    """Driver championship standing"""
    position: int
    driver: Driver
    constructor: Constructor
    points: float
    wins: int


class ConstructorStanding(BaseModel):
    """Constructor championship standing"""
    position: int
    constructor: Constructor
    points: float
    wins: int


class Standings(BaseModel):
    """Championship standings model"""
    season: int
    round: int
    driver_standings: List[DriverStanding]
    constructor_standings: List[ConstructorStanding]
