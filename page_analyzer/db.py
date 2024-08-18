from contextlib import contextmanager
from psycopg2 import pool, OperationalError, InterfaceError
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
db_pool = None


def init_db_pool(database_url):
    global db_pool
    db_pool = pool.SimpleConnectionPool(1, 10, dsn=database_url)


def get_conn():
    if db_pool is None:
        raise Exception("Connection pool is not initialized.")
    return db_pool.getconn()


def release_conn(conn):
    if db_pool:
        db_pool.putconn(conn)


@contextmanager
def get_db_cursor():
    conn = get_conn()
    try:
        try:
            with conn.cursor() as test_cursor:
                test_cursor.execute('SELECT 1')
        except (OperationalError, InterfaceError):
            release_conn(conn)
            conn = get_conn()

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            yield cursor
        conn.commit()
    finally:
        release_conn(conn)


def insert_url(name):
    with get_db_cursor() as cursor:
        cursor.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id',
            (name,)
        )
        url_id = cursor.fetchone()['id']
    return url_id


def get_url_by_id(url_id):
    with get_db_cursor() as cursor:
        cursor.execute(
            'SELECT * FROM urls WHERE id = %s',
            (url_id,)
        )
        url = cursor.fetchone()
    return url


def add_check(url_id, status, h1, title, description):
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO url_checks (
                url_id,
                status,
                h1,
                title,
                description
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                url_id,
                status,
                h1,
                title,
                description
            )
        )


def get_checks(url_id):
    query = """
        SELECT *
        FROM url_checks
        WHERE url_id = %s
        ORDER BY created_at DESC
    """
    value = (url_id,)

    with get_db_cursor() as cursor:
        cursor.execute(query, value)
        all_checks = cursor.fetchall()

    return all_checks


# def get_checked_urls():
#     pass
