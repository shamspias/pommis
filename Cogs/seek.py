import discord
from discord.ext import commands

from Tools.Check import Check

import re


class CogSeek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="seek",
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

        position = divmod(player.position, 60000)
        length = divmod(player.current.length, 60000)

        await ctx.send(
            f"{ctx.author.mention} Current music Seeked to {int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}")


def setup(bot):
    bot.add_cog(CogSeek(bot))
