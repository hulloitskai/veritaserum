import os
import json
import base64

from typing import Dict, Union
from datetime import timedelta

from dotenv import load_dotenv
from reporter import Reporter

if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("MESSENGER_USERNAME")
    password = os.getenv("MESSENGER_PASSWORD")

    session = os.getenv("MESSENGER_SESSION")
    cookies: Dict = None
    if session:
        cookies = json.loads(base64.b64decode(session).decode("utf-8"))

    maxage: Union[str, timedelta] = os.getenv("VERITASERUM_MAXAGE")
    if maxage:
        maxage = timedelta(seconds=int(maxage))

    debug: Union[str, bool] = os.getenv("VERITASERUM_DEBUG")
    if debug:
        debug = debug.lower() in ("true", "yes", "1")

    reporter = Reporter(
        username, password, cookies=cookies, maxage=maxage, debug=debug,
    )
    reporter.listen()
