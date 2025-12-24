import { useState, useEffect } from 'react'
import { Calendar, Trophy, Users, TrendingUp } from 'lucide-react'
import Card from '../components/Card'
import { f1Api } from '../lib/api'
import type { Race, Standings } from '../types'

const Home = () => {
  const [races, setRaces] = useState<Race[]>([])
  const [standings, setStandings] = useState<Standings | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Fetch current season data
        const currentYear = new Date().getFullYear()
        const [racesData, standingsData] = await Promise.allSettled([
          f1Api.getRaces(currentYear),
          f1Api.getStandings(currentYear)
        ])

        if (racesData.status === 'fulfilled') {
          setRaces(racesData.value.slice(-5)) // Last 5 races
        }

        if (standingsData.status === 'fulfilled') {
          setStandings(standingsData.value)
        }
      } catch (err) {
        setError('Failed to fetch data. Please check if the API server is running.')
        console.error('Home page data fetch error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="text-f1-light">Loading dashboard...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <Card title="Error" className="max-w-md">
          <p className="text-red-400">{error}</p>
          <p className="text-sm mt-2 text-f1-light/70">
            Make sure to start the backend API server with: <code>uvicorn app.main:app --reload</code>
          </p>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-f1-light mb-4">
          Welcome to F1 Dashboard
        </h1>
        <p className="text-xl text-f1-light/80">
          Your hub for F1 race results, telemetry, and predictions
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card title="Latest Races" className="lg:col-span-2">
          <div className="flex items-center space-x-2 mb-4">
            <Calendar className="text-f1-red" size={20} />
            <span className="font-medium">Recent Events</span>
          </div>
          
          {races.length > 0 ? (
            <div className="space-y-3">
              {races.map((race) => (
                <div key={`${race.season}-${race.round}`} className="border-l-2 border-f1-red pl-3">
                  <div className="font-medium">{race.race_name}</div>
                  <div className="text-sm text-f1-light/70">
                    {race.circuit_name} • {new Date(race.date).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-f1-light/70">No recent races found</p>
          )}
        </Card>

        <Card title="Championship Leader">
          <div className="flex items-center space-x-2 mb-4">
            <Trophy className="text-f1-red" size={20} />
            <span className="font-medium">Current Leader</span>
          </div>
          
          {standings?.driver_standings[0] ? (
            <div>
              <div className="font-bold text-lg">
                {standings.driver_standings[0].driver.first_name} {standings.driver_standings[0].driver.last_name}
              </div>
              <div className="text-f1-light/70">{standings.driver_standings[0].constructor.name}</div>
              <div className="text-f1-red font-medium mt-2">
                {standings.driver_standings[0].points} points
              </div>
            </div>
          ) : (
            <p className="text-f1-light/70">No standings data</p>
          )}
        </Card>

        <Card title="Quick Stats">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp className="text-f1-red" size={20} />
            <span className="font-medium">This Season</span>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>Races</span>
              <span className="font-medium">{races.length}</span>
            </div>
            <div className="flex justify-between">
              <span>Drivers</span>
              <span className="font-medium">{standings?.driver_standings.length || 0}</span>
            </div>
            <div className="flex justify-between">
              <span>Teams</span>
              <span className="font-medium">{standings?.constructor_standings.length || 0}</span>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Features" className="lg:col-span-2">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 border border-f1-red/20 rounded-lg">
              <Trophy className="text-f1-red mb-2" size={24} />
              <h4 className="font-medium mb-2">Race Explorer</h4>
              <p className="text-sm text-f1-light/70">
                Explore race results, lap times, and telemetry data from past F1 races.
              </p>
            </div>
            
            <div className="p-4 border border-f1-red/20 rounded-lg">
              <TrendingUp className="text-f1-red mb-2" size={24} />
              <h4 className="font-medium mb-2">AI Predictions</h4>
              <p className="text-sm text-f1-light/70">
                Get ML-powered predictions for upcoming qualifying and race sessions.
              </p>
            </div>
          </div>
        </Card>

        <Card title="Getting Started">
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-f1-red rounded-full mt-2 flex-shrink-0"></div>
              <p className="text-sm">Use Race Explorer to browse historical F1 data and telemetry</p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-f1-red rounded-full mt-2 flex-shrink-0"></div>
              <p className="text-sm">Try the Predictions feature for upcoming race forecasts</p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-f1-red rounded-full mt-2 flex-shrink-0"></div>
              <p className="text-sm">Compare driver performance across different metrics</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}

export default Home
