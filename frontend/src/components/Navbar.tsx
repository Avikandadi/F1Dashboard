import { Link, useLocation } from 'react-router-dom'
import { Home, Trophy, Target, BarChart3 } from 'lucide-react'

const Navbar = () => {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/races', label: 'Race Explorer', icon: Trophy },
    { path: '/predictions', label: 'Predictions', icon: Target },
    { path: '/compare', label: 'Compare', icon: BarChart3 },
  ]

  return (
    <nav className="bg-f1-gray border-b border-f1-red">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-f1-red">F1</div>
            <div className="text-xl font-semibold text-f1-light">Dashboard</div>
          </div>
          
          <div className="flex space-x-8">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === path
                    ? 'bg-f1-red text-white'
                    : 'text-f1-light hover:bg-f1-dark hover:text-f1-red'
                }`}
              >
                <Icon size={18} />
                <span>{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
