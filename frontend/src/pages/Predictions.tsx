import { useState } from 'react'
import { Target, TrendingUp, Settings } from 'lucide-react'
import Card from '../components/Card'
import Table from '../components/Table'
import { f1Api } from '../lib/api'
import type { PredictRequest, PredictResponse } from '../types'

const Predictions = () => {
  const [prediction, setPrediction] = useState<PredictResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    season: 2024,
    round: 1,
    session_type: 'qualifying',
    weather_condition: 'Dry',
    track_temperature: 30,
    air_temperature: 25
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      setLoading(true)
      const request: PredictRequest = {
        season: formData.season,
        round: formData.round,
        session_type: formData.session_type,
        weather_condition: formData.weather_condition,
        track_temperature: formData.track_temperature,
        air_temperature: formData.air_temperature
      }
      
      const result = await f1Api.predict(request)
      setPrediction(result)
    } catch (error) {
      console.error('Error generating prediction:', error)
    } finally {
      setLoading(false)
    }
  }

  const predictionColumns = [
    { key: 'predicted_position', label: 'Pos' },
    { 
      key: 'driver', 
      label: 'Driver',
      render: (driver: any) => `${driver.first_name} ${driver.last_name}`
    },
    { 
      key: 'driver', 
      label: 'Team',
      render: (driver: any) => driver.team || 'Unknown'
    },
    { 
      key: 'confidence', 
      label: 'Confidence',
      render: (confidence: number) => `${(confidence * 100).toFixed(1)}%`
    },
    { key: 'reasoning', label: 'Notes' }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3">
        <Target className="text-f1-red" size={32} />
        <h1 className="text-3xl font-bold text-f1-light">AI Predictions</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Prediction Settings" className="lg:col-span-1">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Season</label>
              <input
                type="number"
                value={formData.season}
                onChange={(e) => setFormData({...formData, season: Number(e.target.value)})}
                className="w-full bg-f1-dark text-f1-light px-3 py-2 rounded border border-f1-red/20 focus:border-f1-red focus:outline-none"
                min="2020"
                max="2024"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Round</label>
              <input
                type="number"
                value={formData.round}
                onChange={(e) => setFormData({...formData, round: Number(e.target.value)})}
                className="w-full bg-f1-dark text-f1-light px-3 py-2 rounded border border-f1-red/20 focus:border-f1-red focus:outline-none"
                min="1"
                max="24"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Session Type</label>
              <select
                value={formData.session_type}
                onChange={(e) => setFormData({...formData, session_type: e.target.value})}
                className="w-full bg-f1-dark text-f1-light px-3 py-2 rounded border border-f1-red/20 focus:border-f1-red focus:outline-none"
              >
                <option value="qualifying">Qualifying</option>
                <option value="race">Race</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Weather</label>
              <select
                value={formData.weather_condition}
                onChange={(e) => setFormData({...formData, weather_condition: e.target.value})}
                className="w-full bg-f1-dark text-f1-light px-3 py-2 rounded border border-f1-red/20 focus:border-f1-red focus:outline-none"
              >
                <option value="Dry">Dry</option>
                <option value="Wet">Wet</option>
                <option value="Intermediate">Intermediate</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Track Temp (°C)</label>
                <input
                  type="number"
                  value={formData.track_temperature}
                  onChange={(e) => setFormData({...formData, track_temperature: Number(e.target.value)})}
                  className="w-full bg-f1-dark text-f1-light px-3 py-2 rounded border border-f1-red/20 focus:border-f1-red focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Air Temp (°C)</label>
                <input
                  type="number"
                  value={formData.air_temperature}
                  onChange={(e) => setFormData({...formData, air_temperature: Number(e.target.value)})}
                  className="w-full bg-f1-dark text-f1-light px-3 py-2 rounded border border-f1-red/20 focus:border-f1-red focus:outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-f1-red hover:bg-f1-red/80 disabled:bg-f1-red/50 text-white font-medium py-2 px-4 rounded transition-colors"
            >
              {loading ? 'Generating...' : 'Generate Prediction'}
            </button>
          </form>
        </Card>

        <Card title="Prediction Results" className="lg:col-span-2">
          {prediction ? (
            <div>
              <div className="mb-6">
                <h3 className="text-lg font-medium">{prediction.race_name}</h3>
                <p className="text-f1-light/70 mb-2">{prediction.circuit_name}</p>
                <div className="flex items-center space-x-4 text-sm text-f1-light/70">
                  <span>Session: {prediction.session_type}</span>
                  <span>Model: {prediction.model_info.model_type || 'Unknown'}</span>
                  <span>Generated: {new Date(prediction.generated_at).toLocaleString()}</span>
                </div>
              </div>
              
              <Table columns={predictionColumns} data={prediction.predictions} />
              
              <div className="mt-6 p-4 bg-f1-dark/50 rounded-lg">
                <h4 className="font-medium mb-2 flex items-center">
                  <TrendingUp className="text-f1-red mr-2" size={18} />
                  Model Information
                </h4>
                <div className="text-sm text-f1-light/70 space-y-1">
                  <p>Type: {prediction.model_info.model_type || 'Random Forest'}</p>
                  <p>Version: {prediction.model_info.version || '1.0.0'}</p>
                  {prediction.model_info.features && (
                    <p>Features: {prediction.model_info.features.join(', ')}</p>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-f1-light/70 py-8">
              <Target className="mx-auto mb-4 text-f1-red/50" size={48} />
              <p>Configure your prediction parameters and click "Generate Prediction" to see AI-powered race forecasts.</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}

export default Predictions
