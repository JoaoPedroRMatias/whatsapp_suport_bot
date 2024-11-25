from flask import Flask, request
from src.message import request_message
from src.generate import generate, create_credencials
from src.database import connect_db, chech_remote_jid, create_user
from src.evolution import send_message

app = Flask(__name__)

@app.route('/webhook/messages-upsert', methods=['POST'])
def webhook():
    conn = connect_db()
    data = request.get_json()  
    data = request_message(data)

    print(f"\n{data}", flush=True)

    result = chech_remote_jid(conn, data.remote_jid)
    
    if result == []:
        credencials = create_credencials()
        create_user(conn, data.remote_jid, data.push_name, credencials[0], credencials[1])

        message_genarate = generate(data.mensagem, credencials[1], credencials[0])
        send_message(message_genarate, data.remote_jid)
        return "Mensagem enviada com sucesso"

    else:
        for i in result:
            message_genarate = generate(data.mensagem, i[2], i[3])
            send_message(message_genarate, data.remote_jid)
            return "Mensagem enviada com sucesso"

    return "Retorno com OpenIA desligado.", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
