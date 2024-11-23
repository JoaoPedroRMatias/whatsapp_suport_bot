from flask import Flask, request
from src.message import request_message
from src.generate import generate

app = Flask(__name__)

@app.route('/webhook/messages-upsert', methods=['POST'])
def webhook():
    data = request.get_json()  
    request_message(data)

    message = data.get('message')
    return generate(message), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
