import os
import json

from dotenv import load_dotenv
from fbchat import Client

load_dotenv()
username = os.getenv("MESSENGER_USERNAME")
password = os.getenv("MESSENGER_PASSWORD")

client = Client(
    username,
    password,
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
)
print(json.dumps(client.getSession()))
