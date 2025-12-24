import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface LineChartProps {
  data: any[]
  xKey: string
  yKey: string
  title?: string
  color?: string
  height?: number
}

const F1LineChart = ({ 
  data, 
  xKey, 
  yKey, 
  title, 
  color = '#FF1801', 
  height = 300 
}: LineChartProps) => {
  return (
    <div>
      {title && (
        <h4 className="text-lg font-medium text-f1-light mb-4">{title}</h4>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#38383F" />
          <XAxis 
            dataKey={xKey} 
            stroke="#F7F4F4"
            fontSize={12}
          />
          <YAxis 
            stroke="#F7F4F4"
            fontSize={12}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#38383F',
              border: '1px solid #FF1801',
              borderRadius: '6px',
              color: '#F7F4F4'
            }}
          />
          <Line 
            type="monotone" 
            dataKey={yKey} 
            stroke={color} 
            strokeWidth={2}
            dot={{ fill: color, strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: color, strokeWidth: 2 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default F1LineChart
