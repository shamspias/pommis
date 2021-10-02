import os
# load our local env so we dont have the token in public
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
import validators

from get_songs import GetSongs

from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix='.')  # prefix our commands with '.'

players = {}


def convert_tuple_to_strong(tup):
    st = ' '.join(map(str, tup))
    return st


@client.event  # check if pommis is ready
async def on_ready():
    print('pommis online')


# command for pommis to join the channel of the user,
# if the pommis has already joined and is in a different channel,
# it will move to the channel the user is in
@client.command(aliases=["J", "j"])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
@client.command(aliases=["ply", "P", "p", "Ply", "PLy", "PLY", "pLY", "plY"])
@commands.guild_only()
async def play(ctx, *text):
    url = convert_tuple_to_strong(text)
    await ctx.send(url)
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice:
        await join(ctx)
        voice = get(client.voice_clients, guild=ctx.guild)

    if not validators.url(url):
        song_info = GetSongs.get_from_youtube(url)
        url = song_info[0]
        await ctx.send(song_info[1])

    print(url)
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('pommis is playing')

    # check if the pommis is already playing
    else:
        await ctx.send("pommis is already playing")
        return


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('pommis is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('pommis has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# Command to leave from voice ch
@client.command(aliases=["dc", "DC", "dC", "Dc"])
async def leave(ctx):
    if (ctx.voice_client):  # If the bot is in a voice channel
        await stop(ctx)
        await ctx.guild.voice_client.disconnect()  # Leave the channel
        await ctx.send('Pommis left')
    else:  # But if it isn't
        await ctx.send("I'm not in a voice channel, use the join or j command to make me join")


# command to clear channel messages
@client.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")


client.run(os.getenv('token'))
