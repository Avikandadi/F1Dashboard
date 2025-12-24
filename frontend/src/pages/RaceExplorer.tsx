import { useState, useEffect } from 'react'
import { Search, Calendar } from 'lucide-react'
import Card from '../components/Card'
import Table from '../components/Table'
import LineChart from '../components/LineChart'
import { f1Api } from '../lib/api'
import type { Race, RaceResults, RaceTelemetry } from '../types'

const RaceExplorer = () => {
  const [season, setSeason] = useState(2024)
  const [races, setRaces] = useState<Race[]>([])
  const [selectedRace, setSelectedRace] = useState<number | null>(null)
  const [raceResults, setRaceResults] = useState<RaceResults | null>(null)
  const [telemetry, setTelemetry] = useState<RaceTelemetry | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchRaces()
  }, [season])

  const fetchRaces = async () => {
    try {
      setLoading(true)
      const racesData = await f1Api.getRaces(season)
      setRaces(racesData)
    } catch (error) {
      console.error('Error fetching races:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchRaceData = async (round: number) => {
    try {
      setLoading(true)
      setSelectedRace(round)
      
      const [resultsData, telemetryData] = await Promise.allSettled([
        f1Api.getRaceResults(season, round),
        f1Api.getRaceTelemetry(season, round)
      ])

      if (resultsData.status === 'fulfilled') {
        setRaceResults(resultsData.value)
      }

      if (telemetryData.status === 'fulfilled') {
        setTelemetry(telemetryData.value)
      }
    } catch (error) {
      console.error('Error fetching race data:', error)
    } finally {
      setLoading(false)
    }
  }

  const resultColumns = [
    { key: 'position', label: 'Pos' },
    { 
      key: 'driver', 
      label: 'Driver',
      render: (driver: any) => `${driver.first_name} ${driver.last_name}`
    },
    { 
      key: 'constructor', 
      label: 'Team',
      render: (constructor: any) => constructor.name
    },
    { key: 'points', label: 'Points' },
    { key: 'time', label: 'Time' },
    { key: 'status', label: 'Status' }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-f1-light">Race Explorer</h1>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Calendar className="text-f1-red" size={20} />
            <select
              value={season}
              onChange={(e) => setSeason(Number(e.target.value))}
              className="bg-f1-gray text-f1-light px-3 py-2 rounded border border-f1-red/20 focus:border-f1-red focus:outline-none"
            >
              {[2024, 2023, 2022, 2021, 2020].map((year) => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading && (
        <div className="text-center text-f1-light">Loading...</div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Races" className="lg:col-span-1">
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {races.map((race) => (
              <button
                key={race.round}
                onClick={() => fetchRaceData(race.round)}
                className={`w-full text-left p-3 rounded-lg border transition-colors ${
                  selectedRace === race.round
                    ? 'border-f1-red bg-f1-red/10'
                    : 'border-f1-red/20 hover:border-f1-red/40'
                }`}
              >
                <div className="font-medium">{race.race_name}</div>
                <div className="text-sm text-f1-light/70">
                  Round {race.round} • {race.circuit_name}
                </div>
                <div className="text-xs text-f1-light/50">
                  {new Date(race.date).toLocaleDateString()}
                </div>
              </button>
            ))}
          </div>
        </Card>

        <Card title="Race Results" className="lg:col-span-2">
          {raceResults ? (
            <div>
              <div className="mb-4">
                <h3 className="text-lg font-medium">{raceResults.race.race_name}</h3>
                <p className="text-f1-light/70">{raceResults.race.circuit_name}</p>
              </div>
              <Table columns={resultColumns} data={raceResults.results} />
            </div>
          ) : (
            <p className="text-f1-light/70">Select a race to view results</p>
          )}
        </Card>
      </div>

      {telemetry && telemetry.drivers_telemetry.length > 0 && (
        <Card title="Telemetry Data">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {telemetry.drivers_telemetry.slice(0, 4).map((driverTel) => {
              const speedData = driverTel.telemetry.map((point, index) => ({
                distance: Math.round(point.distance),
                speed: point.speed || 0
              }))

              return (
                <div key={driverTel.driver.code}>
                  <LineChart
                    data={speedData}
                    xKey="distance"
                    yKey="speed"
                    title={`${driverTel.driver.first_name} ${driverTel.driver.last_name} - Speed`}
                    color="#FF1801"
                    height={250}
                  />
                </div>
              )
            })}
          </div>
        </Card>
      )}
    </div>
  )
}

export default RaceExplorer
