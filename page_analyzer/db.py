import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db():
    return psycopg2.connect(DATABASE_URL)


def insert_url(name):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'INSERT INTO urls (name) VALUES (%s) RETURNING id',
        (name,)
    )
    url_id = cursor.fetchone()['id']
    conn.commit()
    conn.close()
    return url_id


def get_url_by_id(url_id):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'SELECT * FROM urls WHERE id = %s',
        (url_id,)
    )
    url = cursor.fetchone()
    conn.commit()
    conn.close()
    return url
