import discord
from discord.ext import commands

from Tools.Check import Check


class CogChangePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="change_prefix",
                      aliases=["cp"],
                      usage="",
                      description="Change Prefix of this server")
    @commands.is_owner()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def change_prefix(self, ctx):
        await ctx.send(f"{ctx.author.mention} Current Prefix of this server changed!")


def setup(bot):
    bot.add_cog(CogChangePrefix(bot))
