interface TableColumn {
  key: string
  label: string
  render?: (value: any, row: any) => React.ReactNode
}

interface TableProps {
  columns: TableColumn[]
  data: any[]
  className?: string
}

const Table = ({ columns, data, className = '' }: TableProps) => {
  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="min-w-full bg-f1-gray rounded-lg overflow-hidden">
        <thead className="bg-f1-red">
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider"
              >
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-f1-red/20">
          {data.map((row, index) => (
            <tr key={index} className="hover:bg-f1-dark/50 transition-colors">
              {columns.map((column) => (
                <td key={column.key} className="px-6 py-4 whitespace-nowrap text-sm text-f1-light">
                  {column.render ? column.render(row[column.key], row) : row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Table
