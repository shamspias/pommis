import os

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("token")
print(token)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


client = MyClient()
client.run(token)
