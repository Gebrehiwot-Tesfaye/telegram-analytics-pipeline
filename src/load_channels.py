import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
PGUSER = os.getenv("POSTGRES_USER")
PGPASS = os.getenv("POSTGRES_PASSWORD")
PGDB = os.getenv("POSTGRES_DB")
PGHOST = os.getenv("POSTGRES_HOST", "localhost")
PGPORT = os.getenv("POSTGRES_PORT", "5432")

engine = create_engine(f"postgresql+psycopg2://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGDB}")

# Load channels.csv into channels table
def load_channels():
    df = pd.read_csv("data/channels.csv")
    df.to_sql("channels", engine, if_exists="replace", index=False)
    print("Loaded channels.csv into channels table.")

if __name__ == "__main__":
    load_channels()
