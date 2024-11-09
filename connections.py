# import os
# import psycopg2
# from dotenv import load_dotenv
#
# load_dotenv()
# def create_connection():
#     return psycopg2.connect(os.environ.get("DATABASE_URI"))



import os
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from contextlib import contextmanager

DB_PROMPT = "Enter Database URL: "
db_uri = input(DB_PROMPT)
if not db_uri:
    load_dotenv()
    db_uri = os.environ["DATABASE_URI"]

pool = SimpleConnectionPool(minconn= 1, maxconn= 5, dsn= db_uri)


@contextmanager
def get_connection():
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)



