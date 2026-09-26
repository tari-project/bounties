import asyncio
from channels.adapters import TelegramChannel, DiscordChannel
from core.knowledge import KnowledgeBase

class SelfLearningBot:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.channels = {
            "telegram": TelegramChannel(token="TG_TOKEN_123"),
            "discord": DiscordChannel(token="DC_TOKEN_456")
        }

    async def process_message(self, channel_name: str, chat_id: str, text: str):
        # Logic for 'Self-Learning'
        if "teach me" in text.lower() or "remember" in text.lower():
            # Extract the knowledge part
            knowledge = text.replace("teach me", "").replace("remember", "").strip()
            self.kb.add_knowledge("general", knowledge)
            response = "Got it! I've learned that. I'll remember it for next time. 🧠"
        else:
            # Retrieve from RAG system
            response = self.kb.query(text)
            response = f"🤖 AI Response: {response}"

        await self.channels[channel_name].send_message(chat_id, response)

    async def run(self):
        print("🚀 Starting Multi-Channel Self-Learning Bot...")
        # In a real app, we would create asyncio tasks for each channel.listen()
        # Here we simulate a turn.
        await self.process_message("telegram", "user_1", "Hello!")
        await self.process_message("telegram", "user_1", "Teach me that the company hours are 9am to 5pm")
        await self.process_message("discord", "user_2", "What are the company hours?")

if __name__ == "__main__":
    bot = SelfLearningBot()
    asyncio.run(bot.run())
