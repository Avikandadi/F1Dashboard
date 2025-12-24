import { BarChart3, Users } from 'lucide-react'
import Card from '../components/Card'

const Compare = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3">
        <BarChart3 className="text-f1-red" size={32} />
        <h1 className="text-3xl font-bold text-f1-light">Driver Comparison</h1>
      </div>

      <Card title="Coming Soon">
        <div className="text-center py-12">
          <Users className="mx-auto mb-4 text-f1-red/50" size={64} />
          <h3 className="text-xl font-medium mb-4">Driver Comparison Feature</h3>
          <p className="text-f1-light/70 mb-6 max-w-md mx-auto">
            Compare driver performance, lap times, and telemetry data across different races and seasons. 
            This feature will be available in a future update.
          </p>
          <div className="bg-f1-dark/50 rounded-lg p-4 max-w-sm mx-auto">
            <h4 className="font-medium mb-2">Planned Features:</h4>
            <ul className="text-sm text-f1-light/70 space-y-1 text-left">
              <li>• Side-by-side driver statistics</li>
              <li>• Lap time comparisons</li>
              <li>• Telemetry overlays</li>
              <li>• Performance trends</li>
              <li>• Head-to-head analysis</li>
            </ul>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default Compare
