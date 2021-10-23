import discord
from discord.ext import commands

from Tools.Check import Check


class CogSeek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="seek",
                      aliases=["seek", "jump"],
                      usage="",
                      description="Seek the current music.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def seek(self, ctx):

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.seek(0)  # Reload the song

        await ctx.send(f"{ctx.author.mention} Current music Seeked!")


def setup(bot):
    bot.add_cog(CogSeek(bot))
