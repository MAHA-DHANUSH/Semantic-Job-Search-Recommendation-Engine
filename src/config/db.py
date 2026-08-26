import os
import psycopg2
from pgvector.psycopg2 import register_vector

DB_CONFIG = dict(
    host=os.getenv("PG_HOST", "localhost"),
    port=int(os.getenv("PG_PORT", 5432)),
    dbname=os.getenv("PG_DB", "postgres"),
    user=os.getenv("PG_USER", "postgres"),
    password=os.getenv("PG_PASS", "postgres"),
)

def connect():
    conn = psycopg2.connect(**DB_CONFIG)
    register_vector(conn)
    return conn
