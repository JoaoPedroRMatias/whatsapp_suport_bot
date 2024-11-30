import psycopg2
from dotenv import load_dotenv
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
        print(f"Erro ao conectar ao banco de dados: {error}", flush=True)
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
        print(f"Erro ao executar a consulta: {error}", flush=True)
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
        print(f"Erro ao inserir o registro: {error}", flush=True)
        return False

    finally:
        if cursor:
            cursor.close()


def similar_search(message, conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT instrumento, finalidade, tema_assunto, juris, adequada_a_nll, 
               base_legal_nllc, base_legal_llc, link_da_peca, temas_boletim_tc_numero, palavra_chave
        FROM jurisprudencia_tribunais
    """)    
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    textos = [f"{row[1]} {row[2]} {row[3]} {row[4]}" for row in rows]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(textos)

    message_vector = vectorizer.transform([message])

    similarities = cosine_similarity(message_vector, tfidf_matrix)

    similar_indices = similarities.argsort()[0][-3:][::-1]

    similar_rows = [rows[i] for i in similar_indices]
    return similar_rows