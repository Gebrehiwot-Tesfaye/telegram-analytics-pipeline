import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
PGUSER = os.getenv("POSTGRES_USER")
PGPASS = os.getenv("POSTGRES_PASSWORD")
PGDB = os.getenv("POSTGRES_DB")
PGHOST = os.getenv("POSTGRES_HOST", "localhost")
PGPORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGDB}"
engine = create_engine(DATABASE_URL)