import discord
from discord.ext import commands

from Tools.Check import Check

import aiohttp
import datetime as dt


class CogLyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    LYRICS_URL = "https://some-random-api.ml/lyrics?title="

    @commands.command(name="lyrics",
                      aliases=["lyric", "Lyric"],
                      usage="",
                      description="Lyrics for current music.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def lyrics(self, ctx):

        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return

        name = player.current.title.replace("*", "\\*")

        async with ctx.typing():
            async with aiohttp.request("GET", self.LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    return await ctx.send("Lyrics Not Found!")

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    return await ctx.send(f"<{data['links']['genius']}>")

                embed = discord.Embed(
                    title=data["title"],
                    description=data["lyrics"],
                    colour=ctx.author.colour,
                    timestamp=dt.datetime.utcnow(),
                )
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"])
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogLyrics(bot))
