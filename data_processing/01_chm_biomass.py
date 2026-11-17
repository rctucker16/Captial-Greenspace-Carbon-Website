# Create a list of directions for writing a set of code for chm biomass in a python env to be uploaded for connecting to final web design

# Pipeline Specification: `01_chm_biomass.py`

## Overview
This document outlines the architecture, data dependencies, and implementation steps for the `01_chm_biomass.py` script. This script forms the core of our spatial data pipeline, extracting Canopy Height Model (CHM) statistics across all **21 Edinburgh study sites**, calibrating allometric biomass equations against ground-truth field plots, and writing site-level carbon stock metrics into our Oracle database.

---

## 1. Environment & Dependencies
Ensure your virtual environment has the following geospatial and database libraries installed:
* Python 3.10+
* `rasterio`
* `geopandas`
* `rioxarray` (or `rasterstats`)
* `numpy`
* `pandas`
* `scikit-learn`
* `oracledb`

---

## 2. Implementation Steps

1. **Coordinate Reference System (CRS) Verification**
   * Load the LiDAR CHM raster and verify its CRS is **EPSG:27700** (OSGB36 / British National Grid).
   * Query study site polygons (`cgs_greenspace`) and field plots (`cgs_field_plot`) from Oracle, reprojecting to `EPSG:27700` if necessary.

2. **Raster Cleaning & Thresholding**
   * Filter out `NoData` values and ground-level noise. Set any CHM pixel heights below **2.0 meters** to `0` to prevent low shrubs and non-tree objects from inflating canopy metrics.

3. **Field Plot Extraction & Allometric Calibration**
   * Buffer each field plot coordinate (`x_coord`, `y_coord`) by its exact `radius_m`.
   * Extract zonal CHM metrics per plot (mean height, max height, sum of heights, canopy cover percentage).
   * Fit/validate a linear regression model against field-measured plot carbon (`cgs_plot_carbon`). Log $R^2$ and $\text{RMSE}$ metrics to the console.

4. **Site-Level Scaling Across the 21 Study Sites**
   * Clip the cleaned CHM raster to each of the 21 greenspace polygons.
   * Calculate total canopy area ($\text{m}^2$), canopy percentage, mean height, and estimated Above-Ground Biomass (AGB).
   * Convert AGB to **Carbon Stock ($\text{kg C}$)** using the standard IPCC conversion factor ($\text{AGB} \times 0.47$).

5. **Oracle Database Write-back**
   * Use parameterized SQL (`oracledb` bind variables) to upsert results into the Oracle database tables (`greenspace_id_name_carbon_result` and `cgs_site_carbon`).

---

## 3. Starter Code Template

```python
"""
01_chm_biomass.py
Extracts LiDAR CHM metrics across 21 Edinburgh greenspace study sites,
calibrates/applies allometric biomass-to-carbon models against field plots,
and writes site-level carbon stock results to Oracle.
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from sklearn.linear_model import LinearRegression
import oracledb

# Constants
TARGET_CRS = "EPSG:27700"
MIN_TREE_HEIGHT_M = 2.0
CARBON_FRACTION = 0.47  # Standard IPCC AGB to Carbon conversion factor


def get_oracle_connection():
    """Connects to Oracle using environment variables."""
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )


def extract_zonal_chm_stats(geom, src_raster):
    """Clips CHM raster to a polygon geometry and computes canopy metrics."""
    out_image, _ = mask(src_raster, [geom], crop=True, nodata=np.nan)
    data = out_image[0]
    valid = data[~np.isnan(data)]
    
    if valid.size == 0:
        return {"canopy_pct": 0.0, "mean_height_m": 0.0, "sum_height_m": 0.0, "canopy_area_m2": 0.0}

    canopy_pixels = valid[valid >= MIN_TREE_HEIGHT_M]
    pixel_area_m2 = abs(src_raster.transform[0] * src_raster.transform[4])

    return {
        "canopy_pct": float((canopy_pixels.size / valid.size) * 100.0),
        "mean_height_m": float(np.mean(canopy_pixels)) if canopy_pixels.size > 0 else 0.0,
        "sum_height_m": float(np.sum(canopy_pixels)),
        "canopy_area_m2": float(canopy_pixels.size * pixel_area_m2)
    }


def compute_site_carbon(sites_gdf, src_raster):
    """Computes AGB and Carbon Stock (kg C) for all 21 study sites."""
    results = []
    for _, row in sites_gdf.iterrows():
        stats = extract_zonal_chm_stats(row.geometry, src_raster)
        
        # Placeholder allometric formula
        estimated_agb_kg = stats["sum_height_m"] * 12.5  
        carbon_stock_kg = estimated_agb_kg * CARBON_FRACTION

        results.append({
            "greenspace_id": row["greenspace_id"],
            "carbon_stock_kg_carbon": round(carbon_stock_kg, 2),
            "canopy_pct": round(stats["canopy_pct"], 2),
            "mean_height_m": round(stats["mean_height_m"], 2)
        })
    return pd.DataFrame(results)


def write_results_to_oracle(results_df, conn):
    """Upserts site-level carbon metrics into Oracle tables."""
    cursor = conn.cursor()
    sql = """
        MERGE INTO greenspace_id_name_carbon_result target
        USING (SELECT :1 AS greenspace_id, :2 AS carbon_val FROM dual) src
        ON (target.greenspace_id = src.greenspace_id)
        WHEN MATCHED THEN
            UPDATE SET target.carbon_stock_kg_carbon = src.carbon_val
        WHEN NOT MATCHED THEN
            INSERT (greenspace_id, carbon_stock_kg_carbon)
            VALUES (src.greenspace_id, src.carbon_val)
    """
    try:
        rows = [(r["greenspace_id"], r["carbon_stock_kg_carbon"]) for _, r in results_df.iterrows()]
        cursor.executemany(sql, rows)
        conn.commit()
        print(f"Successfully wrote {len(rows)} site carbon records to Oracle.")
    finally:
        cursor.close()


if __name__ == "__main__":
    pass
