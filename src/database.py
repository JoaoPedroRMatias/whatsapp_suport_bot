import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


def connect_db():
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        return conn

    except Exception as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None


def search_user(conn):
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM whatsapp_user_information LIMIT 5;")
        rows = cursor.fetchall()

        return rows

    except Exception as error:
        print(f"Erro ao executar a consulta: {error}")
        return None

    finally:
        if cursor:
            cursor.close()


conn = connect_db()



