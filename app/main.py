from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import notifications
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kalos Notification Service",
    description="Slack notification service for Kalos platform",
    version="0.0.1",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notifications.router)


@app.get("/")
def read_root():
    return {
        "service": "Kalos Notification Service",
        "status": "running",
        "version": "0.0.1",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
