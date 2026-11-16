# App entry point & CORS configuration

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_queries import fetch_greenspace_with_plot_carbon

app = FastAPI(
  title="Edinburgh Capital Greenspace WebGIS API",
  description""Backend APi serving Oracle Spatial data for Edinburgh greenspaces, carbon stock, and field plots. ",
  version= "1,0,0"
)

# Configures CORS (Cross-Origin Resource SHaring)
# This allows frontend (running locally or in a browser) to query the API smoothly.
app.add.middleware(
CORSMiddleware,
allow_origins=["*"], When writing restrict this to own specific frontend domain 
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Health check endpoint to verify the API is running."""
    return {
        "status": "online",
        "message": "Welcome to the Edinburgh Capital Greenspace API"
    }

@app.get("/api/greenspaces")
def get_greenspaces():
"""

API endpoint that fetches all Edinburgh greenspaces joined with Elin's field plot carbon data and environmnetal deprivation results. """

try:
    data = fetch_greenspace_with_plot_carbon()
    return {
        "status": "success",
        "count": len(data),
        "data": data
    }
except Exception as e:
    return {
        "status": "error" ,
        "message": str(e),
        "data": []
    }
