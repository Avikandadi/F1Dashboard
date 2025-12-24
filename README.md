# F1 Dashboard - Results & Predictions MVP

A full-stack application for Formula 1 race analysis, historical data exploration, and AI-powered predictions.

![F1 Dashboard](https://img.shields.io/badge/F1-Dashboard-red?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?style=flat-square)
![React](https://img.shields.io/badge/React-18-blue?style=flat-square)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-yellow?style=flat-square)

## 🏎️ Features

### 📊 **Dashboard Home**
- Recent race results and upcoming events
- Current championship standings
- Quick statistics and key metrics
- Feature overview and navigation

### 🏁 **Race Explorer**
- Browse historical F1 race data by season
- Detailed race results with driver and constructor information
- Interactive telemetry charts showing speed, throttle, brake data
- Lap time analysis and fastest lap tracking

### 🤖 **AI Predictions**
- Machine learning-powered qualifying predictions
- Configurable race parameters (weather, temperature, track conditions)
- Confidence scores and prediction reasoning
- Model information and feature analysis

### 📈 **Performance Analytics**
- Real-time data from FastF1 API
- SQLite caching for improved performance
- Responsive design for desktop and mobile
- Interactive charts and visualizations

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **FastF1** - Official F1 timing data and telemetry
- **SQLite** - Lightweight database with caching
- **scikit-learn** - Machine learning predictions
- **Pydantic** - Data validation and serialization
- **pytest** - Comprehensive testing suite

### Frontend
- **React 18** - Modern React with hooks and TypeScript
- **Vite** - Lightning-fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Beautiful and responsive charts
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **Git** for cloning the repository

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd f1Dashboard
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload
```

The backend API will be available at: **http://localhost:8000**

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: **http://localhost:5173**

### 4. Verify Installation
- **Backend Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **Frontend Dashboard**: http://localhost:5173

## 📁 Project Structure

```
f1Dashboard/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry
│   │   ├── api/            # API route handlers
│   │   ├── models/         # Pydantic data models
│   │   ├── services/       # Business logic services
│   │   ├── core/           # Configuration and settings
│   │   └── db/             # Database schema
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── lib/            # API client and utilities
│   │   └── types.ts        # TypeScript definitions
│   ├── package.json        # Node.js dependencies
│   └── README.md          # Frontend documentation
└── README.md              # This file
```

## 🔧 Development

### API Endpoints

#### Health & Info
- `GET /health` - Health check
- `GET /` - API information

#### Race Data
- `GET /api/races/{season}` - Get all races for a season
- `GET /api/race/{season}/{round}/results` - Get race results
- `GET /api/race/{season}/{round}/telemetry` - Get telemetry data
- `GET /api/standings/{season}` - Get championship standings

#### Predictions
- `POST /api/predict` - Generate AI predictions

### Environment Configuration

Create `.env` files for custom configuration:

**Backend (.env)**:
```bash
DATABASE_URL=sqlite:///./f1_dashboard.db
ENABLE_CACHE=true
CACHE_TTL_HOURS=24
FASTF1_CACHE_DIR=./fastf1_cache
```

**Frontend (.env)**:
```bash
VITE_API_URL=http://localhost:8000
```

### Testing

**Backend Tests**:
```bash
cd backend
pytest tests/ -v
```

**Frontend Development**:
```bash
cd frontend
npm run lint        # Code linting
npm run build       # Production build
npm run preview     # Preview build
```

## 📊 Usage Examples

### Fetching Race Data
```python
# Get 2024 season races
races = await f1Api.getRaces(2024)

# Get specific race results
results = await f1Api.getRaceResults(2024, 1)  # Bahrain GP
```

### Generating Predictions
```typescript
const prediction = await f1Api.predict({
  season: 2024,
  round: 5,
  session_type: "qualifying",
  weather_condition: "Dry",
  track_temperature: 35,
  air_temperature: 28
})
```

## 🎯 Acceptance Criteria ✅

- [x] `GET /health` returns `{status:"ok"}`
- [x] `GET /races/{season}` returns non-empty race data
- [x] Race explorer renders table + interactive charts
- [x] `POST /predict` returns ranked top-10 predictions
- [x] App runs fully with `uvicorn` + `npm run dev`
- [x] Clean, responsive UI with F1 theming
- [x] TypeScript throughout frontend
- [x] Comprehensive error handling
- [x] Caching for performance optimization

## 🚀 Deployment

### Production Build

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run build
# Serve dist/ directory with your preferred web server
```

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure backend is running on port 8000
   - Check CORS configuration in `main.py`
   - Verify frontend API base URL in `api.ts`

2. **FastF1 Data Loading Slow**
   - First-time data downloads can be slow
   - FastF1 cache will improve subsequent requests
   - Consider pre-warming cache for better UX

3. **Build Errors**
   - Clear caches: `rm -rf node_modules .venv`
   - Reinstall dependencies
   - Check Python/Node versions

### Performance Tips

- Enable backend caching for faster API responses
- FastF1 data is cached locally after first download
- Use appropriate cache TTL values for different data types
- Monitor API response times in browser dev tools

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- **FastF1** - For providing excellent F1 data access
- **Formula 1** - For the amazing sport and data
- **React & FastAPI** communities for great tools and documentation

---

**Built with ❤️ for Formula 1 fans and data enthusiasts**
