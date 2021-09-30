import os

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("token")

client = discord.Client()


@client.event
async def on_message(message):
    message.content.lower()
    if message.author == client.user:
        return
    if message.content.startwith("hello"):
        await message.channel.send("Hi, Your bot is here")


client.run(token)
