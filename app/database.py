import time

import psycopg
from psycopg.connection import Connection
from psycopg.rows import DictRow, dict_row

from app.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def connect():
    conn = psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            row_factory=dict_row
        )
    return conn

def cursor(conn: Connection[DictRow]):
    cur = conn.cursor()
    return cur


while True:
    try:
        conn = connect()
        cur = cursor(conn)
    except Exception as E:
        print(f"Connecting to Database Failed: {E}")
        time.sleep(2)
    else:
        print("Connected to Database Successfully")
        break