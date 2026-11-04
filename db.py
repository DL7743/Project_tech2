import os
 
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
 
load_dotenv()
 
 
def connect_db():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("Добавьте DATABASE_URL в файл .env")
    return psycopg.connect(url, row_factory=dict_row)
