"""
🛡️ Mangifera Shield — Main Server
FastAPI backend for the Mangifera Shield AgriTech platform.
Serves the PWA frontend and provides API endpoints for:
- AI Disease Detection (ResNet50)
- Khet-Khata Inventory Ledger
- Mandi Price Discovery
- Weather Disease Alerts
- Quality Certificate Generation
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from .database import init_db
from .routes import disease, ledger, mandi, weather, certificate

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Create FastAPI app
app = FastAPI(
    title="🛡️ Mangifera Shield API",
    description="AI-powered mango disease detection & farm management for Malihabad",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(disease.router)
app.include_router(ledger.router)
app.include_router(mandi.router)
app.include_router(weather.router)
app.include_router(certificate.router)

# Serve frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

    # Serve TF.js model files for browser AI inference
    models_dir = os.path.join(FRONTEND_DIR, "models")
    if os.path.exists(models_dir):
        app.mount("/models", StaticFiles(directory=models_dir), name="models")

    # Serve manifest and service worker from root
    @app.get("/manifest.json")
    async def serve_manifest():
        return FileResponse(os.path.join(FRONTEND_DIR, "manifest.json"))

    @app.get("/sw.js")
    async def serve_sw():
        return FileResponse(
            os.path.join(FRONTEND_DIR, "sw.js"),
            media_type="application/javascript"
        )

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/api/health")
async def health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "app": "Mangifera Shield",
        "version": "1.0.0",
        "features": [
            "AI Disease Detection",
            "Khet-Khata Ledger",
            "Mandi Prices",
            "Weather Alerts",
            "Quality Certificates",
            "Voice Navigation"
        ]
    }


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()
    print("🛡️ Mangifera Shield server started!")
    print("📊 Database initialized")
    print(f"🌐 Frontend: {FRONTEND_DIR}")
    print("📖 API Docs: http://localhost:8000/api/docs")
