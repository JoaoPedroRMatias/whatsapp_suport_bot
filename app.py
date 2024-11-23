from flask import Flask, request
from src.message import request_message
from src.generate import generate
from src.database import connect_db

app = Flask(__name__)

@app.route('/webhook/messages-upsert', methods=['POST'])
def webhook():
    data = request.get_json()  
    data = request_message(data)

    print(data.remote_jid)

    #message = data.get('message')
    #return generate(message), 200
    return "Retorno com OpenIA desligado.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
