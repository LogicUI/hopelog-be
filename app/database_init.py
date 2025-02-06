from psycopg2 import pool
from dotenv import load_dotenv
import os
import logging


# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Environment variables
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
dbname = os.getenv("DBNAME")


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create connection pool
try:
    db_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user=user,
        password=password,
        host=host,
        port=port,
        database=dbname,
    )
    if db_pool:
        logging.info("Connection pool created successfully.")
except Exception as e:
    logging.error(f"Error creating connection pool: {e}")
    raise e


# Dependency to provide a connection
def get_db_connection():
    connection = db_pool.getconn()
    try:
        yield connection
    finally:
        db_pool.putconn(connection)
