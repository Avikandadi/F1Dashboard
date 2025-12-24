-- F1 Dashboard Database Schema

-- Races table
CREATE TABLE IF NOT EXISTS races (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER NOT NULL,
    round INTEGER NOT NULL,
    race_name TEXT NOT NULL,
    circuit_name TEXT NOT NULL,
    date DATE NOT NULL,
    time TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(season, round)
);

-- Race results table
CREATE TABLE IF NOT EXISTS race_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    race_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    driver_id TEXT NOT NULL,
    constructor_id TEXT NOT NULL,
    points REAL DEFAULT 0,
    time TEXT,
    status TEXT,
    fastest_lap TEXT,
    fastest_lap_rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (race_id) REFERENCES races(id)
);

-- Drivers table
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    permanent_number INTEGER,
    nationality TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Constructors table
CREATE TABLE IF NOT EXISTS constructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    constructor_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    nationality TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cache table (already created in cache_service.py)
CREATE TABLE IF NOT EXISTS cache (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions log table
CREATE TABLE IF NOT EXISTS prediction_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER NOT NULL,
    round INTEGER NOT NULL,
    session_type TEXT NOT NULL,
    request_data TEXT,
    prediction_data TEXT,
    model_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
