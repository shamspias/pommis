import discord
from discord.ext import commands

from Tools.Check import Check

import re


class CogSeek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="seeks",
                      aliases=["seeks", "jump"],
                      usage="",
                      description="Seek the current music.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def seek_new(self, ctx, position: str):

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return

        TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
        if not (match := re.match(TIME_REGEX, position)):
            await ctx.send(f"{ctx.author.mention} Please Provide valid time. Example: 10s")

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.seek(secs * 1000)  # seek the song with second

        await ctx.send(f"{ctx.author.mention} Current music Seeked!")


def setup(bot):
    bot.add_cog(CogSeek(bot))
