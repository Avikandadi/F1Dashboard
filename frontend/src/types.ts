// Type definitions for API responses

export interface Driver {
  driver_id: string
  first_name: string
  last_name: string
  code: string
  permanent_number?: number
  team?: string
}

export interface Constructor {
  constructor_id: string
  name: string
  nationality: string
}

export interface RaceResult {
  position: number
  driver: Driver
  constructor: Constructor
  points: number
  time?: string
  status: string
  fastest_lap?: string
  fastest_lap_rank?: number
}

export interface Race {
  season: number
  round: number
  race_name: string
  circuit_name: string
  date: string
  time?: string
  url?: string
}

export interface RaceResults {
  race: Race
  results: RaceResult[]
}

export interface TelemetryPoint {
  distance: number
  speed?: number
  throttle?: number
  brake?: boolean
  gear?: number
  rpm?: number
  drs?: boolean
}

export interface DriverTelemetry {
  driver: Driver
  lap_number: number
  lap_time?: string
  telemetry: TelemetryPoint[]
}

export interface RaceTelemetry {
  race: Race
  drivers_telemetry: DriverTelemetry[]
}

export interface DriverStanding {
  position: number
  driver: Driver
  constructor: Constructor
  points: number
  wins: number
}

export interface ConstructorStanding {
  position: number
  constructor: Constructor
  points: number
  wins: number
}

export interface Standings {
  season: number
  round: number
  driver_standings: DriverStanding[]
  constructor_standings: ConstructorStanding[]
}

export interface PredictRequest {
  season: number
  round: number
  session_type: string
  weather_condition?: string
  track_temperature?: number
  air_temperature?: number
}

export interface DriverPrediction {
  driver: Driver
  predicted_position: number
  confidence: number
  reasoning?: string
}

export interface PredictResponse {
  session_type: string
  race_name: string
  circuit_name: string
  predictions: DriverPrediction[]
  model_info: Record<string, any>
  generated_at: string
}
