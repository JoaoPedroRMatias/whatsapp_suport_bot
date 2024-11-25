from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()


def create_credencials():
    thread = client.beta.threads.create()
    thread_id = thread.id

    assistant = client.beta.assistants.create(
        name="Dr Licita",
        instructions="Você é um advogado focado em licitações.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o",
    )

    credencials = [thread_id, assistant.id]
    return credencials


def generate(message, assistant_id, thread_id):
    client.beta.threads.messages.create(
        thread_id= thread_id,
        role="user",
        content=message,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id= thread_id,
        assistant_id= assistant_id,
        instructions="Trate o usuário com formalidade."
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id= thread_id)
        
        messages_sorted = sorted(messages, key=lambda msg: msg.created_at, reverse=True)
        last_message = messages_sorted[0]
        last_message_text = last_message.content[0].text.value

        return last_message_text

    else:
        print(f"Status do processamento: {run.status}", flush=True)
