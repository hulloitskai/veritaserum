import re
import requests
import logging

from copy import deepcopy
from typing import List, Dict
from logging import Logger
from datetime import timedelta, datetime

import fbchat
from fbchat import Client, User, Message, Mention, ThreadType


class Reporter(Client):
    debug: bool
    logger: Logger
    maxage: timedelta
    messages: Dict[str, Message] = dict()

    def __init__(
        self,
        username: str,
        password: str,
        cookies: Dict,
        maxage=timedelta(hours=1),
        debug=False,
    ) -> None:
        level = logging.DEBUG if debug else logging.INFO
        client_level = logging.INFO if debug else logging.ERROR

        logger = Logger(Reporter.__name__, level)
        logger.addHandler(logging.StreamHandler())
        logger.info("Authenticating client...")

        super(Reporter, self).__init__(
            username,
            password,
            session_cookies=cookies,
            logging_level=client_level,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
        )
        self.setDefaultThread(self.uid, ThreadType.USER)
        logger.info("Client authenticated.")

        self.debug = debug
        self.logger = logger
        self.maxage = maxage
        self.messages = dict()

    def __clean(self) -> bool:
        self.logger.info("Cleaning up expired messages...")
        now = datetime.now()

        discarded = 0
        messages: Dict[str, Message] = dict()
        for id, message in self.messages.items():
            timestamp = datetime.fromtimestamp(message.timestamp / 1000)
            timestamp += timedelta(milliseconds=(message.timestamp % 1000))

            if now > (timestamp + self.maxage):
                discarded += 1
            else:
                messages[id] = message

        if discarded:
            self.logger.info(f"Discarded {discarded} messages.")
            self.messages = messages
            return True

        self.logger.info("No expired messages.")
        return False

    __counter = 0

    def onMessage(
        self, mid: str, message: str, author_id: str, message_object: Message, **kwargs,
    ) -> None:
        if not self.debug:
            if author_id == self.uid:
                return

        self.logger.debug(f"Received message: {message}")
        self.logger.debug(f"Cached messages: {len(self.messages)}")

        self.messages[mid] = message_object
        self.__counter += 1
        if self.__counter >= 60:
            self.__counter = 0
            self.__clean()

    def onMessageUnsent(self, mid: str, author_id: str, **kwargs) -> None:
        if not self.debug:
            if author_id == self.uid:
                return

        author: User = self.fetchUserInfo(author_id)[author_id]
        name = author.name
        self.logger.info(f"Caught unsend by {name}.")

        message = Message(
            f"{name} unsent a message.",
            mentions=[Mention(author_id, length=len(name))],
        )
        id = self.send(message)

        if mid not in self.messages:
            return

        message: Message = deepcopy(self.messages[mid])
        message.reply_to_id = id

        files = Reporter.__message_files(message)
        if files:
            self.sendRemoteFiles(files, message)
        else:
            self.send(message)

    @staticmethod
    def __message_files(message: Message) -> List[str]:
        files = list()
        for a in message.attachments:
            if isinstance(a, fbchat.ImageAttachment):
                if a.is_animated:
                    files.append(a.animated_preview_url)
                else:
                    url = a.large_preview_url or a.preview_url or a.thumbnail_url
                    if url:
                        files.append(url)
            elif isinstance(a, fbchat.VideoAttachment):
                files.append(a.preview_url)
            elif isinstance(a, fbchat.FileAttachment):
                r = requests.get(a.url)
                if r.status_code == 200:
                    url = re.search(
                        r'document\.location\.replace\("(.*)"\);', r.text,
                    ).group(1)
                    url = url.replace(r"\/", "/")
                    files.append(url)
        return files
