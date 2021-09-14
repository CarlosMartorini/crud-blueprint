import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

configs = {
    "host": os.environ.get("DB_HOST"),
    "database": os.environ.get("DB_DATABASE"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
}


def open_connection():
    return psycopg2.connect(**configs)


def close_connection(conn, cur):
    conn.commit()
    cur.close()
    conn.close()