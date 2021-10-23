import discord
from discord.ext import commands

from Tools.Check import Check


class CogLyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lyrics",
                      aliases=["lyric", "Lyric"],
                      usage="",
                      description="Lyrics for current music.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def lyrics(self, ctx):

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return

        await ctx.send(f"{ctx.author.mention} Lyrics for Current music reload!")


def setup(bot):
    bot.add_cog(CogLyrics(bot))
