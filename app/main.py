
from fastapi import FastAPI

# Create JARVIS application
app = FastAPI(
    title="JARVIS",
    description="Personal AI Assistant",
    version="0.1.0"
)


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
