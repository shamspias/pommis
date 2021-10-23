import discord
from discord.ext import commands

import aiohttp
import json
import datetime as dt


class CogAnimes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    PAT_URL = "https://some-random-api.ml/pat"
    HUG_URL = "https://some-random-api.ml/hug"
    WINK_URL = "https://some-random-api.ml/wink"

    @commands.command(name="pats",
                      aliases=["pat", "pet", "pets", "Pats", "Pet"],
                      usage="",
                      description="Pats")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def pats(self, ctx, other="<@Pommis#3767>"):
        async with aiohttp.request("GET", self.PAT_URL, headers={}) as r:
            data = await r.json(content_type="text/html")

        await ctx.send(
            f"{ctx.author.mention} Pats so adorable to {other}")

        await ctx.send(data["link"])

    @commands.command(name="hugs",
                      aliases=["hug", "Hug", "hugggg"],
                      usage="",
                      description="Hugs")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def hugs(self, ctx, other="<@Pommis#3767>"):
        async with aiohttp.request("GET", self.HUG_URL, headers={}) as r:
            data = await r.read()

        data = json.loads(data)

        await ctx.send(
            f"{ctx.author.mention} Hugs {other}")

        await ctx.send(data["link"])

    @commands.command(name="winks",
                      aliases=["Wink", "wink", "wimp"],
                      usage="",
                      description="winkss")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def winks(self, ctx, other="<@Pommis#3767>"):
        async with aiohttp.request("GET", self.WINK_URL, headers={}) as r:
            data = await r.json(content_type="text/html")

            await ctx.send(
                f"{ctx.author.mention} Wink {other}")

            await ctx.send(data["link"])


def setup(bot):
    bot.add_cog(CogAnimes(bot))
