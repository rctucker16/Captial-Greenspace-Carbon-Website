import geopandas as gpd
import pandas as pd

TARGET_CRS = "EPSG: 27700"
WEB_CRS = "EPSG: 4326"

def load_sites_and_plots(
  sites_path: str,
  plots_csv_path: str,
  deprivation_path
