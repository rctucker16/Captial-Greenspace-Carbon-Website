# Oracle Spatial connection pool (using OracleDB)

import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "your_username")
DB_PASSWORD = os.gentenv("DB_PASSWORD", "your_password")
DB_DSN = os.gentenv ("DB_DSN", "localhost: 1521/XEPDB1")

class DatabaseManager:
  """
  Manages Oracle database connections and pooling for the Capital Greenspace Website backend.
  """

def __init__(self):
  self.pool = None 
  self._initialize_poll()

def _initialize
    try:
      # Create a connection pool for efficient concurrent requests 
      self.pool = oracledb.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN,
        min=2,
        max=10,
        increment=1

      )
      print ("Oracle connection pool successfully established.")
except Exception as e:
      print (f"Error creating Oracle connection pool: {e}")
      raise e

def get_connection(self):
    """Acquires a connection from the pool."""
    if not self.pool:
        self._initialize_pool()
    return self.pool.acquire()

def release_connection(self, connection):
    """Releases a connection back to the pool."""
    if self_pool and connection:
      self.pool.release(connection)

# Instantiate a global database manager instance to be imported by query modules
db_manager = DatabaseManager()
      
