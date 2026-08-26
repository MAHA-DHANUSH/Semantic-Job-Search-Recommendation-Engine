import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_CONFIG = dict(
    host=os.getenv("PG_HOST", "localhost"),
    port=int(os.getenv("PG_PORT", 5432)),
    dbname=os.getenv("PG_DB", "jobsdb"),
    user=os.getenv("PG_USER", "postgres"),
    password=os.getenv("PG_PASS", "postgres"),
)

def setup_db():
    # Connect to the default postgres database to create jobsdb
    default_config = DB_CONFIG.copy()
    default_config["dbname"] = "postgres"
    
    try:
        conn = psycopg2.connect(**default_config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_CONFIG['dbname']}'")
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE DATABASE {DB_CONFIG['dbname']}")
                print(f"Created database {DB_CONFIG['dbname']}")
            else:
                print(f"Database {DB_CONFIG['dbname']} already exists")
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        return

    # Now connect to the jobsdb and run setup.sql
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            with open("setup.sql", "r") as f:
                sql = f.read()
                cur.execute(sql)
                print("Database setup complete.")
        conn.close()
    except Exception as e:
        print(f"Error running setup.sql: {e}")

if __name__ == "__main__":
    setup_db()
