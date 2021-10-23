import discord
from discord.ext import commands

from Tools.Check import Check

import ksoftapi


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

        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return

        query = player.current.track.title.replace("*", "\\*")

        kclient = ksoftapi.Client('AIzaSyAAg3GHxipuyDz7KsCAv434yoFT56TR9LQ')

        try:
            results = await kclient.music.lyrics(query)
        except ksoftapi.NoResults:
            print('No lyrics found for ' + query)
        else:
            first = results[0]
            embed = discord.Embed(title=f"** [{query}] **", description=f"**[{first.lyrics}]**",
                                  color=discord.Colour.random())
            await ctx.send(embed=embed)

        await ctx.send(f"{ctx.author.mention} Lyrics for Current music!")


def setup(bot):
    bot.add_cog(CogLyrics(bot))
