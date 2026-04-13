import os
from abc import ABC, abstractmethod

class MessageChannel(ABC):
    @abstractmethod
    async def send_message(self, chat_id: str, text: str):
        pass

    @abstractmethod
    async def listen(self, callback):
        pass

class TelegramChannel(MessageChannel):
    def __init__(self, token):
        self.token = token
        # In a real impl, we'd use aiogram or python-telegram-bot
        print(f"Telegram Channel initialized with token {token[:5]}***")

    async def send_message(self, chat_id: str, text: str):
        print(f"[Telegram] Sending to {chat_id}: {text}")

    async def listen(self, callback):
        print("[Telegram] Listening for messages...")
        # Mock loop
        pass

class DiscordChannel(MessageChannel):
    def __init__(self, token):
        self.token = token
        print(f"Discord Channel initialized with token {token[:5]}***")

    async def send_message(self, chat_id: str, text: str):
        print(f"[Discord] Sending to {chat_id}: {text}")

    async def listen(self, callback):
        print("[Discord] Listening for messages...")
        pass
