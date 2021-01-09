import discord
import asyncio

def sendPlayingSongEmbed(self, ctx, music):
    # Send message
    requestedBy =  music["requestedBy"]
    music =  music["music"]
    
    if music.isLive:
        duration = "Live"
    else:
        musicDurationSeconds = music.duration % 60
        if musicDurationSeconds < 10:
            musicDurationSeconds = f"0{musicDurationSeconds}"
        duration = f"{music.duration//60}:{musicDurationSeconds}"

    music.title = music.title.replace("*", "\\*")

    embed=discord.Embed(title="Playing Song :", description=f"**[{music.title}]({music.url})**", color=discord.Colour.random())
    embed.set_thumbnail(url=music.thumbnails)
    embed.add_field(name="Requested by :", value=f"> {requestedBy}", inline=True)
    embed.add_field(name="Duration :", value=f"> {duration}", inline=True)
    embed.add_field(name="Volume :", value=f"> " + str(round(self.bot.music[ctx.guild.id]["volume"]*100)) + "%", inline=True)
    embed.add_field(name="Loop :", value=f"> " + str(self.bot.music[ctx.guild.id]["loop"]), inline=True)
    embed.add_field(name="Lyrics :", value=f"> {self.bot.command_prefix}lyrics", inline=True)
    embed.add_field(name="Queue :", value=f"> "+ str(len(self.bot.music[ctx.guild.id]["musics"])) + " song(s) in the queue", inline=True)
    embed.add_field(name="DJ Role :", value=f"> @role", inline=True)
    asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.bot.loop)