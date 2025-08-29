import os, json
from azure.storage.queue import QueueClient

queue_name = os.getenv("WELCOME_QUEUE", "welcome-emails")
queue_conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

queue_client = QueueClient.from_connection_string(queue_conn, queue_name)

def enqueue_welcome(payload: dict):
    queue_client.send_message(json.dumps(payload))
