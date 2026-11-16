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
  columns = [col[0].lower() for col in 
