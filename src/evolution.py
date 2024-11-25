import requests
from dotenv import load_dotenv
import os


load_dotenv()

def send_message(message_genarate, remote_jid):
    try:
        url = "http://evolution-api:8080/message/sendText/suporte_bot"
        headers = {
            "apikey": f"{os.getenv('AUTHENTICATION_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "number": f"{remote_jid}",
            "options": {
                "delay": 1200,
                "presence": "composing"
            },
            "textMessage": {
                "text": f"{message_genarate}"
            }
        }

        response = requests.post(url, headers=headers, json=data)

        print(f"Status Code: {response.status_code}", flush=True)
        print(f"Response: {response.text}", flush=True)

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}", flush=True)
    except Exception as e:
        print(f"Erro inesperado: {e}", flush=True)
