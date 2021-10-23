import discord
from discord.ext import commands

import aiohttp
import datetime as dt


class CogJocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    JOCKS_URL = "https://some-random-api.ml/joke"

    @commands.command(name="jocks",
                      aliases=["jock", "jokes", "jocke"],
                      usage="",
                      description="Show random jocks")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def jocks(self, ctx):
        async with ctx.typing():
            async with aiohttp.request("GET", self.JOCKS_URL, headers={}) as r:
                data = await r.json()

                embed = discord.Embed(
                    title="Sonics Bully",
                    description=data["joke"],
                    colour=ctx.author.colour,
                    timestamp=dt.datetime.utcnow(),
                )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogJocks(bot))
