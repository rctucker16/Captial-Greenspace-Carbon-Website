# Pydantic data validation schemas 

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GreenspaceBase (BaseModel): 
  """API response wrapper for a single or multiple greenspace records."""
  status: str = Field(default="success", description="Status of the API request")
  count: int = Field(..., description="Number of greenspace records returned")
  data: List[GreenspaceBase] = Field(..., description="List of greenspace records with carbon metrics")

class GeoJSONFeature(BaseModel):
  """Pydantic model representing a standard GeoJSON Feature."""
  type: str = Field(default="Feature")
  geometry: Dict [str, Any] = Field(..., description="GeoJSON geometry dictionary (Polygon or MultiPolyogn)")
  properties: Dict[str, Any] = Field(..., description="Associated attribute data (name, carbon stock, deprivation)")

class GeoJSONFeatureCollection(BaseModel):
  """Pydantic model representing a standard GeoJSON Feature."""
  type: str = Field(default="FeatureCollection")
  features: List[GeoJSONFeature] = Field(..., description="List of geographic features to render on the map")
