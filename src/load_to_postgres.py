import os
import json
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()
PGUSER = os.getenv("POSTGRES_USER")
PGPASS = os.getenv("POSTGRES_PASSWORD")
PGDB = os.getenv("POSTGRES_DB")
PGHOST = os.getenv("POSTGRES_HOST", "localhost")
PGPORT = os.getenv("POSTGRES_PORT", "5432")

def load_json_to_postgres(json_path, table_name, conn):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_sql(table_name, conn, if_exists='append', index=False, method='multi')

if __name__ == "__main__":
    import sqlalchemy
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGDB}")
    pre_dir = "data/preprocessed"
    for date_dir in os.listdir(pre_dir):
        full_dir = os.path.join(pre_dir, date_dir)
        for file in os.listdir(full_dir):
            if file.endswith(".json"):
                path = os.path.join(full_dir, file)
                table = "raw_telegram_messages"
                print(f"Loading {path} into {table}")
                load_json_to_postgres(path, table, engine)