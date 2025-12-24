import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import RaceExplorer from './pages/RaceExplorer'
import Predictions from './pages/Predictions'
import Compare from './pages/Compare'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-f1-dark text-f1-light">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/races" element={<RaceExplorer />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/compare" element={<Compare />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
