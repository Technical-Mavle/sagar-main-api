# In sagar-main-api/backend_router.py

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from config import supabase
import os

# --- NEW: Import the function directly from the ML router ---
from ml_router import create_geospatial_correlation_job, CorrelationRequest

router = APIRouter()

# --- Pydantic Models ---
class OrchestrationRequest(BaseModel):
    file1_id: int
    file2_id: int
    column1: str
    column2: str
    file1_lat_col: str = "decimalLatitude"
    file1_lon_col: str = "decimalLongitude"
    file2_lat_col: str = "lat"
    file2_lon_col: str = "lon"

# --- Main Endpoints ---
@router.post("/discover-and-correlate")
async def discover_and_correlate_data(request: OrchestrationRequest, background_tasks: BackgroundTasks):
    """
    Finds file paths from the database and triggers the ML service for analysis.
    """
    try:
        # 1. Query the database to get the file paths from their IDs
        print(f"Fetching metadata for file IDs {request.file1_id} and {request.file2_id}")
        query = supabase.table('file_metadata').select("id, processed_file_location")
        query = query.in_('id', [request.file1_id, request.file2_id])
        db_response = query.execute()

        if not db_response.data or len(db_response.data) < 2:
            raise HTTPException(status_code=404, detail="One or both file IDs not found in the database.")

        file_map = {item['id']: item['processed_file_location'] for item in db_response.data}
        
        # 2. Prepare the request model for the ML service function
        ml_request = CorrelationRequest(
            file1_path=file_map[request.file1_id],
            file2_path=file_map[request.file2_id],
            column1=request.column1,
            column2=request.column2,
            file1_lat_col=request.file1_lat_col,
            file1_lon_col=request.file1_lon_col,
            file2_lat_col=request.file2_lat_col,
            file2_lon_col=request.file2_lon_col
        )

        # 3. NEW: Call the ML service function directly
        print("Calling ML service function directly...")
        ml_job_data = await create_geospatial_correlation_job(ml_request, background_tasks)

        return {
            "message": "Successfully dispatched job to ML service.",
            "ml_service_response": ml_job_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/search")
async def search_metadata(file_type: str | None = None):
    """Searches the file_metadata table."""
    try:
        query = supabase.table('file_metadata').select("*")
        if file_type:
            query = query.eq('file_type', file_type)
        response = query.execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")