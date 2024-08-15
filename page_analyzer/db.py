import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db(database_url):
    return psycopg2.connect(database_url)
