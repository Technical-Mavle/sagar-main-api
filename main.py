# In sagar-main-api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the routers from your other files
from orchestrator_router import router as orchestrator_router
from backend_router import router as backend_router
from ml_router import router as ml_router

app = FastAPI(
    title="SAGAR Unified API",
    description="A single, high-performance service for data discovery, orchestration, and analysis."
)

# Add CORS middleware to the main app to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the routers into the main application
# All endpoints will be available under a single URL
app.include_router(orchestrator_router, tags=["Orchestrator"])
app.include_router(backend_router, tags=["Backend"])
app.include_router(ml_router, tags=["ML Service"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "SAGAR Unified API is running."}