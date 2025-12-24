"""
F1 Dashboard FastAPI Application

This is the main entry point for the F1 Results & Predictions API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_races import router as races_router
from app.api.routes_predict import router as predict_router
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="F1 Dashboard API",
    description="API for F1 race results, telemetry, and predictions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(races_router, prefix="/api")
app.include_router(predict_router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "F1 Dashboard API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
