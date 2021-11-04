import discord
from discord.ext import commands

import json
from youtubesearchpython import Video, ResultMode

from DataBase.Playlist import DBPlaylist

from Tools.addTrack import addTrack


class CogPlaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="playlist", aliases=["pl"], invoke_without_command=True)
    async def playlist(self, ctx):
        pass
    
    @playlist.command(name="display",
                      aliases=["dis", "spl", "dpl"],
                      usage="",
                      description="Show your playlist")
    @commands.guild_only()
    async def playlist_display(self, ctx):
        playlistNameContent = DBPlaylist(self.bot.dbConnection).display_playlist_names(ctx.author.id)  # Request

        if len(playlistNameContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} You have no playlist!")

        isFirstMessage = True
        message = ""
        playlistNameContent = set(playlistNameContent)
        for number, i in enumerate(playlistNameContent, start=1):
            message += f"**{number}) [{i[0]}]({i[0]})**\n"
            if len(message) > 1800:

                if isFirstMessage:
                    embedTitle = "Playlist Names :"
                    isFirstMessage = False
                else:
                    embedTitle = ""

                embed = discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
                embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                message = ""
        if len(message) > 0:
            embedTitle = f"Playlist :" if isFirstMessage else ""
            embed = discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    
    @playlist.command(name="remove_playlist_name",
                      aliases=["plr", "pl_remove", "rpl", "PLR", "RPL"],
                      usage="<Index>",
                      description="Remove a playlist")
    @commands.guild_only()
    async def playlist_name_remove(self, ctx, index):

        index = int(index) - 1

        playlistContent = DBPlaylist(self.bot.dbConnection).display_playlist_names(ctx.author.id)  # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist is empty!")

        if index < 0 or index > (len(playlistContent) - 1):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The index is available!")
        
        playlistContent = list(set(playlistContent))

        DBPlaylist(self.bot.dbConnection).remove_playlist(ctx.author.id , playlistContent[index][0])  # Request

        embed = discord.Embed(title=f"Your Playlist has been removed",
                              description=f"- ** {playlistContent[index][0]} Deleted **", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


    @playlist.command(name="add",
                      aliases=[],
                      usage="<YouTubeLink>",
                      description="Add a song to your playlist")
    @commands.guild_only()
    async def playlist_add(self, ctx, pl_name, link):
        if not link.startswith("https://www.youtube.com/watch"):
            return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")
        # Check if the link exists
        track = await self.bot.wavelink.get_tracks(link)
        track = track[0]
        if track is None:
            return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")

        playlistSize = DBPlaylist(self.bot.dbConnection).countPlaylistItems(ctx.author.id, pl_name)  # Request
        if playlistSize >= 25:
            return await ctx.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is full (25 songs)!")
        DBPlaylist(self.bot.dbConnection).add(ctx.author.id, pl_name, track.title, track.uri)  # Request

        embed = discord.Embed(title="Song added in your playlist", description=f"- **[{track.title}]({track.uri})**",
                              color=discord.Colour.random())
        embed.add_field(name="playlist name :", value=pl_name, inline=True)
        embed.add_field(name="playlist size :", value=f"`{playlistSize + 1}/25`", inline=True)
        embed.set_thumbnail(url=track.thumb)
        embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @playlist.command(name="show",
                      aliases=["view"],
                      usage="",
                      description="Show your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_show(self, ctx, pl_name):
        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, pl_name)  # Request

        if len(playlistContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is empty!")

        isFirstMessage = True
        message = ""
        for number, i in enumerate(playlistContent, start=1):
            message += f"**{number}) [{i[2]}]({i[3]})**\n"
            if len(message) > 1800:

                if isFirstMessage:
                    embedTitle = f"{pl_name} Playlist :"
                    isFirstMessage = False
                else:
                    embedTitle = ""

                embed = discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
                embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                message = ""
        if len(message) > 0:
            embedTitle = f"{pl_name} Playlist :" if isFirstMessage else ""

            embed = discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @playlist.command(name="remove",
                      aliases=["delete"],
                      usage="<Index>",
                      description="Remove a song of your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_remove(self, ctx, pl_name, index):

        index = int(index) - 1

        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, pl_name)  # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is empty!")

        if index < 0 or index > (len(playlistContent) - 1):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The index is available!")
        DBPlaylist(self.bot.dbConnection).remove(ctx.author.id, pl_name , playlistContent[index][3])  # Request

        embed = discord.Embed(title=f"Song removed from your playlist ({pl_name})",
                              description=f"- **[" + playlistContent[index][2] + "](" + playlistContent[index][
                                  3] + ")**", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @playlist.command(name="load",
                      aliases=[],
                      usage="",
                      description="Load all songs of your playlist in the queue")
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def playlist_load(self, ctx, pl_name):

        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, pl_name)  # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is empty!")

        links = [i[3] for i in playlistContent]
        await addTrack(self, ctx, links)


def setup(bot):
    bot.add_cog(CogPlaylist(bot))
