import json
from database import db_manager 

def fetch_greenspace_carbon_metrics():

""" Queries Oracle, joining greenspace metadata with their calculated carbon stock results. """
connection = db_manager.get_connection()
cursor = connection.cursor()

sql = """
SELECT
    gs.greenspace_id,
    gs.site_name,
    gs.site_type,
    COALESCE(carbon.carbon_stock_kg_carbon, 0) AS carbon_stock_kg_carbon
FROM greenspace_id_name gs
LEFT JOIN greenspace_is_name_carbon_result carbon
    ON gs.greenspace_is = carbon.greenspace_id
ORDER BY gs.greenspace_id
"""

try:
  cursor.execute(sql)
  columns = [col[0].lower() for col in cursor.description]
  return [dict(zip(columns, row)) for row in cursor.fetchall()]
except Exception as e:
    print(f"Error in fetch_greenspace_carbon_metrics: {e}")
    return []
finally:
    cursor.close()
    db_manager.release_connection(connection)

def fetch_greenspaces_geojson():
    """ Queries Oracle Spatial, converting SDO_GEOMETRY polygons into standard GeoJSON format for the Leaflet map frontend. """

    connection = db_manager.get_connection()
    cursor = connection.cursor()

    sql = """
        SELECT
            g.greenspace_id,
            g.site_name,
            g.site_type,
            g.area_m2,
            COALESCE (c.carbon_stock_kg_carbon, 0) AS carbon_stock_kg_carbon,
            SDO_UTIL.TO_GEOJSON(g.goem) AS geojson_geom
        FROM cgs_greenspace g
        LEFT JOIN cgs_site_carbon c ON g.greenspace_id = c.greenspace_id 
    """

    try: 
        cursor.execute(sql)
        columns = [col[0].lower() for col in cursor.description]

        features = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            geom_str = row_dict.pop('geojson_geom', None)

            if geom_str:
                geom_json = json.loads(geom_str)
                feature = {
                    "type": "Feature",
                    "geometry": geom_json,
                    "properties": row_dict
                {
                features.append(feature)
    execept Exception as e:
        print(f"Error in fetch_greenspaces_geojson: {e}")
        return {"type": "FeatureCollection", "features": []}
    finally: 
        cursor.close()
        db.manager.release_connection(connection)

def fetch_environmental_deprivation():
    """
    Queries environmental deprivation scores, canopy percentages,
    and deprivation classes linked to data zones.
    """
    connection = db_manager.get_connection()
    cursor = connection.cursor()

sql = """
    SELECT 
        z.czone
