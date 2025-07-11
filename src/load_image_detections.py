import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv()
PGUSER = os.getenv("POSTGRES_USER")
PGPASS = os.getenv("POSTGRES_PASSWORD")
PGDB = os.getenv("POSTGRES_DB")
PGHOST = os.getenv("POSTGRES_HOST", "localhost")
PGPORT = os.getenv("POSTGRES_PORT", "5432")

engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGDB}")

df = pd.read_json("data/image_detections.json")
df.to_sql("image_detections", engine, if_exists="append", index=False, method="multi")