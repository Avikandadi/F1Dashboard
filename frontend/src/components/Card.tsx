import { ReactNode } from 'react'

interface CardProps {
  title: string
  children: ReactNode
  className?: string
}

const Card = ({ title, children, className = '' }: CardProps) => {
  return (
    <div className={`bg-f1-gray rounded-lg p-6 shadow-lg border border-f1-red/20 ${className}`}>
      <h3 className="text-xl font-semibold text-f1-light mb-4">{title}</h3>
      <div className="text-f1-light">
        {children}
      </div>
    </div>
  )
}

export default Card
