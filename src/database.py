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


def chech_remote_jid(conn, remote_jid):
    try:
        cursor = conn.cursor()

        query = """
        SELECT * 
        FROM whatsapp_user_information
        WHERE remote_jid = %s;
        """
        cursor.execute(query, (remote_jid,)) 
        rows = cursor.fetchall()

        return rows

    except Exception as error:
        print(f"Erro ao executar a consulta: {error}")
        return None

    finally:
        if cursor:
            cursor.close()


def create_user(conn, remote_jid, push_name, id_thread, id_assistance):
    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO whatsapp_user_information (remote_jid, id_assistance, id_thread, push_name)
        VALUES (%s, %s, %s, %s);
        """

        cursor.execute(query, (remote_jid, id_assistance, id_thread, push_name))

        conn.commit()
        return True

    except Exception as error:
        print(f"Erro ao inserir o registro: {error}")
        return False

    finally:
        if cursor:
            cursor.close()