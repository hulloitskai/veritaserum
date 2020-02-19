import os
from .reporter import Reporter
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("MESSENGER_USERNAME")
    password = os.getenv("MESSENGER_PASSWORD")
    reporter = Reporter(username, password)
    reporter.listen()
