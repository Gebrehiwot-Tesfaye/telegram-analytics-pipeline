import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
PGUSER = os.getenv("POSTGRES_USER")
PGPASS = os.getenv("POSTGRES_PASSWORD")
PGDB = os.getenv("POSTGRES_DB")
PGHOST = os.getenv("POSTGRES_HOST", "localhost")
PGPORT = os.getenv("POSTGRES_PORT", "5432")

try:
    conn = psycopg2.connect(
        dbname=PGDB,
        user=PGUSER,
        password=PGPASS,
        host=PGHOST,
        port=PGPORT
    )
    print("✅ Successfully connected to the PostgreSQL database!")
    conn.close()
except Exception as e:
    print(f"❌ Failed to connect to the database: {e}")
