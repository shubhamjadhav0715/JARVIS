
from fastapi import FastAPI

from app.api.conversations import router as conversations_router


# Create JARVIS application
app = FastAPI(
    title="JARVIS",
    description="Personal AI Assistant",
    version="0.2.0"
)

# Register API routes
app.include_router(conversations_router)


@app.get("/")
async def home():
    return {
        "assistant": "JARVIS",
        "message": "Hello! JARVIS is online.",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "assistant": "JARVIS"
    }
