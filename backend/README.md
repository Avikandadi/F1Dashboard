# F1 Dashboard - Backend API

A FastAPI-based backend service providing F1 race data, telemetry, and ML-powered predictions.

## Features

- **Race Data**: Historical race results, lap times, and telemetry
- **Standings**: Driver and constructor championship standings
- **Predictions**: AI-powered qualifying and race predictions
- **Caching**: SQLite-based caching for improved performance
- **FastF1 Integration**: Direct access to Formula 1 timing data

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern web framework for APIs
- **FastF1** - Formula 1 timing data and telemetry
- **SQLite** - Lightweight database for caching
- **Pydantic** - Data validation and serialization
- **scikit-learn** - Machine learning predictions
- **pytest** - Testing framework

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   ```bash
   # On macOS/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred settings
   ```

### Running the API

1. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **The API will be available at**: `http://localhost:8000`

3. **Interactive API documentation**: `http://localhost:8000/docs`

4. **Health check**: `http://localhost:8000/health`

## API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /` - API information

### Race Data
- `GET /api/races/{season}` - Get all races for a season
- `GET /api/race/{season}/{round}/results` - Get race results
- `GET /api/race/{season}/{round}/telemetry` - Get race telemetry
- `GET /api/standings/{season}` - Get championship standings

### Predictions
- `POST /api/predict` - Generate AI predictions

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=app --cov-report=html
```

## Configuration

Environment variables (optional):

```bash
# Database
DATABASE_URL=sqlite:///./f1_dashboard.db

# Cache Configuration
ENABLE_CACHE=true
CACHE_TTL_HOURS=24

# FastF1 Configuration
FASTF1_CACHE_DIR=./fastf1_cache

# ML Model Configuration
MODEL_PATH=./models

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173
```

## Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── routes_races.py  # Race-related endpoints
│   │   └── routes_predict.py # Prediction endpoints
│   ├── models/
│   │   ├── race.py         # Pydantic models for race data
│   │   └── predict.py      # Pydantic models for predictions
│   ├── services/
│   │   ├── fastf1_service.py # FastF1 data service
│   │   ├── ml_service.py    # ML prediction service
│   │   └── cache_service.py # Caching service
│   ├── core/
│   │   └── config.py       # Configuration settings
│   └── db/
│       └── schema.sql      # Database schema
├── tests/
│   ├── test_health.py      # Health endpoint tests
│   └── test_predict.py     # Prediction tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md              # This file
```

### Adding New Features

1. **Add new endpoints** in `app/api/`
2. **Create Pydantic models** in `app/models/`
3. **Implement business logic** in `app/services/`
4. **Add tests** in `tests/`
5. **Update documentation**

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the correct directory and virtual environment is activated
2. **FastF1 cache issues**: Delete the `fastf1_cache` directory and restart
3. **Port conflicts**: Change the port with `uvicorn app.main:app --reload --port 8001`

### Performance Tips

- Enable caching for better response times
- Use appropriate cache TTL values
- Monitor FastF1 data downloads (they can be slow initially)

## License

This project is for educational and demonstration purposes.
