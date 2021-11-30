import discord
import wavelink
from discord.ext import commands
from math import ceil

from Tools.Check import Check

from DataBase.Skip import DBSkip


class CogSkipTo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skipto",
                      aliases=["s_to", "sto"],
                      usage="",
                      description="Skip music to specific position.")
    @commands.guild_only()
    async def skip_to(self, ctx, index):

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return

        if not ctx.author.guild_permissions.administrator:

            users = DBSkip(self.bot.dbConnection).displayUsers(ctx.guild.id)
            usersCount = len(users)

            # If user had already skip
            if ctx.author.id in [i[0] for i in users]:
                return await ctx.send(
                    f"{ctx.author.mention} Waiting for other voice users! ({usersCount}/{ceil(len(ctx.author.voice.channel.voice_states) / 2)})")

            # Add to the DB
            DBSkip(self.bot.dbConnection).add(ctx.guild.id, ctx.author.id)
            usersCount += 1

            # Calcul the ratio
            ratio = usersCount / (len(ctx.author.voice.channel.voice_states) - 1) * 100  # It's a percentage
            if not ratio > 50:
                return await ctx.send(
                    f"{ctx.author.mention} Waiting for other voice users! ({usersCount}/{ceil(len(ctx.author.voice.channel.voice_states) / 2)})")

        # Clean the dict
        DBSkip(self.bot.dbConnection).clear(ctx.guild.id)
        await ctx.send(f"{ctx.author.mention} music skiped to !")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.seek(player.current.duration)


def setup(bot):
    bot.add_cog(CogSkipTo(bot))
