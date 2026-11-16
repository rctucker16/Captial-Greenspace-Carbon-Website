# API endpoints (e.g., /api/sites)

from fastapi import API Router, HTTPException
from typing import List
from models import GreenspaceBase, GreenspaceResponse
from db_queries import fetch_greenspace_carbon_metrics

# Initialize the APIRouter
router = APIRouter(
  prefix="/api/greenspaces",
  tags=["Greenspaces & Carbon Metrics"]
)

@router.get("/", response_model=GreenspaceResponse)
def get_all_greenspaces():
    """ Retrieve all Edinburgh greenspaces joined with their carbon stock results and environmental deprivation metrics."""

    try:
      data = fetch_greenspace_carbon_metrics()
      return {
          "status": "success",
          "count": len(data),
          "data": data
      }
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Database error: {str(e)}

@router.get("/{greenspace_id}", response_model=GreenspaceBase)
def get_greenspace_by_id(greenspace_id: str):
    """ Retrieve metrics for a single specific greenspace by its ID. """

data = fetch_greenspace_carbon_metrics()
match = next((item for item in data if item["greenspace_id"] == greenspace_id), None)

if not match:
  raise HTTPExeception(status_code=404, detail=f"Greenspace with ID '{greenspace_id}' not found.")

return match
  
