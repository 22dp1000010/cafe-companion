from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routers import chat, wait_time, matching
from app.config import settings

app = FastAPI(
    title="Café Companion API",
    description="AI-powered café experience with ordering, recommendations, wait-time prediction, and customer matching",
    version="1.0.0",
)

# Include routers
app.include_router(chat.router)
app.include_router(wait_time.router)
app.include_router(matching.router)

# Mount static files (frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
async def root():
    """Serve the frontend."""
    frontend_index = os.path.join(frontend_path, "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)
    return {
        "message": "Café Companion API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    from app.firebase import is_firebase_configured

    return {
        "status": "healthy",
        "firebase_configured": is_firebase_configured(),
        "gemini_configured": bool(settings.gemini_api_key),
        "environment": settings.environment,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )
