import axios from 'axios'
import type { 
  Race, 
  RaceResults, 
  RaceTelemetry, 
  Standings, 
  PredictRequest, 
  PredictResponse 
} from '../types'

// Base API configuration
const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// API functions
export const f1Api = {
  // Health check
  async healthCheck() {
    const response = await axios.get('http://localhost:8000/health')
    return response.data
  },

  // Get races for a season
  async getRaces(season: number): Promise<Race[]> {
    const response = await api.get(`/races/${season}`)
    return response.data
  },

  // Get race results
  async getRaceResults(season: number, round: number): Promise<RaceResults> {
    const response = await api.get(`/race/${season}/${round}/results`)
    return response.data
  },

  // Get race telemetry
  async getRaceTelemetry(season: number, round: number, lap: number = 1): Promise<RaceTelemetry> {
    const response = await api.get(`/race/${season}/${round}/telemetry?lap=${lap}`)
    return response.data
  },

  // Get standings
  async getStandings(season: number, round?: number): Promise<Standings> {
    const url = round ? `/standings/${season}?round=${round}` : `/standings/${season}`
    const response = await api.get(url)
    return response.data
  },

  // Generate predictions
  async predict(request: PredictRequest): Promise<PredictResponse> {
    const response = await api.post('/predict', request)
    return response.data
  },
}

export default f1Api
