class MessageData:
    def __init__(self, evento, instancia, destino, remote_jid, from_me, message_id,
                 push_name, mensagem, message_type, timestamp, owner, source):
        self.evento = evento
        self.instancia = instancia
        self.destino = destino
        self.remote_jid = remote_jid
        self.from_me = from_me
        self.message_id = message_id
        self.push_name = push_name
        self.mensagem = mensagem
        self.message_type = message_type
        self.timestamp = timestamp
        self.owner = owner
        self.source = source

    def __str__(self):
        return (f"Evento: {self.evento}\n"
                f"Instância: {self.instancia}\n"
                f"Destino: {self.destino}\n"
                f"Remote JID: {self.remote_jid}\n"
                f"From Me: {self.from_me}\n"
                f"Message ID: {self.message_id}\n"
                f"Push Name: {self.push_name}\n"
                f"Mensagem: {self.mensagem}\n"
                f"Message Type: {self.message_type}\n"
                f"Timestamp: {self.timestamp}\n"
                f"Owner: {self.owner}\n"
                f"Source: {self.source}")
    
    
def request_message(data):
    evento = data.get('event')
    instancia = data.get('instance')
    destino = data.get('destination')
    dados_principais = data.get('data', {})
    remote_jid = dados_principais.get('key', {}).get('remoteJid')
    from_me = dados_principais.get('key', {}).get('fromMe')
    message_id = dados_principais.get('key', {}).get('id')
    push_name = dados_principais.get('pushName')
    mensagem = dados_principais.get('message', {}).get('conversation')
    message_type = dados_principais.get('messageType')
    timestamp = dados_principais.get('messageTimestamp')
    owner = dados_principais.get('owner')
    source = dados_principais.get('source')

    message_data = MessageData(evento, instancia, destino, remote_jid, from_me, message_id,
                               push_name, mensagem, message_type, timestamp, owner, source)

    return message_data