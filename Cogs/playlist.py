import discord
from discord.ext import commands

import json
from youtubesearchpython import Video, ResultMode

from DataBase.Playlist import DBPlaylist
from DataBase.Queue import DBQueue

from Tools.addTrack import addTrack

from Cogs.play import (
    searchSpotifyTrack,
    searchSpotifyPlaylist,
    searchDeezer,
    searchSoundcloud,
    searchQuery,
    searchPlaylist,
)

class CogPlaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="playlist", aliases=["pl"], invoke_without_command=True)
    async def playlist(self, ctx):
        pass
    
    @playlist.command(name="display",
                      aliases=["dis", "spl", "dpl", "view", "v", "V", "View"],
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
                      aliases=["plr", "pl_remove", "remove_pl", "rpl", "PLR", "RPL", "delete_pl", "pl_delete"],
                      usage="<Index>",
                      description="Remove a playlist")
    @commands.guild_only()
    async def playlist_name_remove(self, ctx, index):
        
        try:
            index = int(index) - 1
        except:
            return await ctx.send("Please Enter Playlist Index Number")
        playlistContent = DBPlaylist(self.bot.dbConnection).display_playlist_names(ctx.author.id)  # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist is empty!")

        if index < 0 or index > (len(playlistContent) - 1):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The index is available!")
        
        playlistContent = list(set(playlistContent))

        try:
            DBPlaylist(self.bot.dbConnection).remove_playlist(ctx.author.id , playlistContent[index][0])  # Request
            embed = discord.Embed(title=f"Your Playlist has been removed",
            description=f"- ** {playlistContent[index][0]} Deleted **", color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            
        except:
            await ctx.channel.send("Already Deleted or Enter valade Index")

        
    ### Start Add To Playlist ###

    @playlist.command(name="add",
                      aliases=[],
                      usage="<YouTubeLink>",
                      description="Add a song to your playlist")
    @commands.guild_only()
    async def playlist_add(self, ctx, pl_name, *args):
        
        args = " ".join(args)

        with open("configuration.json", "r") as config:
            data = json.load(config)
            self.playlistLimit = int(data.get("playlistLimit", 100))
            # 0 is nolimit
            print(f"Playlist limit set to {self.playlistLimit}")

        # Spotify
        if args.startswith("https://open.spotify.com"):
            if args.startswith("https://open.spotify.com/track"):
                args = await searchSpotifyTrack(self, ctx, args)
            elif args.startswith("https://open.spotify.com/playlist"):
                args = await searchSpotifyPlaylist(self, ctx, args)
            else:
                return await ctx.send(
                    f"{self.bot.emojiList.false} {ctx.author.mention} Only Spotify playlist and Spotify track are available!")
            if args is None: return

        # Deezer
        elif args.startswith("https://deezer.page.link") or args.startswith("https://www.deezer.com"):
            args = await searchDeezer(self, ctx, args)
            if args is None:
                return

        # SoundCloud
        elif args.startswith("https://soundcloud.com"):
            args = await searchSoundcloud(self, ctx, args)
            if args is None: return

        # Youtube Playlist
        elif args.startswith("https://www.youtube.com/playlist"):
            args = await searchPlaylist(self, ctx, args)
            if args is None: return

        # YouTube video
        elif args.startswith("https://www.youtube.com/watch"):
            await ctx.send(" Searching...", delete_after=10)
            # Check if the link exists
            track = await self.bot.wavelink.get_tracks(args)
            args = track[0]
            if track is None:
                return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")

        # Query
        else:
            args = await searchQuery(self, ctx, args)
            if args is None: return

        track = args
        
        
        if isinstance(track, list):
            for trk in track:
                if trk is None:
                    return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")

                playlistSize = DBPlaylist(self.bot.dbConnection).countPlaylistItems(ctx.author.id, pl_name)  # Request
                if playlistSize >= 100:
                    return await ctx.send(
                        f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is full (100 songs)!")
                DBPlaylist(self.bot.dbConnection).add(ctx.author.id, pl_name, trk.title, trk.uri)  # Request
            
            await ctx.channel.send("Playlist Added")
        
        else:

            if track is None:
                return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")

            playlistSize = DBPlaylist(self.bot.dbConnection).countPlaylistItems(ctx.author.id, pl_name)  # Request
            if playlistSize >= 100:
                return await ctx.send(
                    f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is full (100 songs)!")
            DBPlaylist(self.bot.dbConnection).add(ctx.author.id, pl_name, track.title, track.uri)  # Request

            embed = discord.Embed(title="Song added in your playlist", description=f"- **[{track.title}]({track.uri})**",
                                color=discord.Colour.random())
            embed.add_field(name="playlist name :", value=pl_name, inline=True)
            embed.add_field(name="playlist size :", value=f"`{playlistSize + 1}/100`", inline=True)
            embed.set_thumbnail(url=track.thumb)
            embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)


    ### End Add To Playlist ###

    @playlist.command(name="show",
                      aliases=["shows"],
                      usage="",
                      description="Show your playlist")
    @commands.guild_only()
    
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
    
    async def playlist_remove(self, ctx, pl_name, index):

        index = int(index) - 1

        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, pl_name)  # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is empty!")

        if index < 0 or index > (len(playlistContent) - 1):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The index is available!")
        
        try:
            DBPlaylist(self.bot.dbConnection).remove(ctx.author.id, pl_name , playlistContent[index][3])  # Request
        except:
            await ctx.channel.send("Already Deleted or Enter valade Index")

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

    async def playlist_load(self, ctx, pl_name):

        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, pl_name)  # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(
                f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist ({pl_name}) is empty!")

        links = [i[3] for i in playlistContent]
        await addTrack(self, ctx, links)

    
    # @commands.command(name="move",
    #                   usage="<IndexFrom> <IndexTo>",
    #                   description="Move a song in the playlist.")
    # @commands.guild_only()
    # 
    # async def move(self, ctx, pl_name, indexFrom, indexTo):

    #     try:
    #         tracks = DBQueue(self.bot.dbConnection).display(ctx.guild.id)
    #         tracksCount = len(tracks)
    #         if len(tracks) == 0:
    #             return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The queue is empty!")
    #     except:
    #         await ctx.send("Problem with track")

    #     if not indexFrom.isdigit() or not indexTo.isdigit():
    #         return await ctx.channel.send(f"{self.bot.emojiList.false}{ctx.author.mention} Index have to be a number!")
    #     if ((int(indexFrom)) > tracksCount) or ((int(indexTo)) > tracksCount):
    #         return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} Index is invalid!")
    #     if (int(indexFrom) == int(indexTo)):
    #         return await ctx.channel.send(
    #             f"{self.bot.emojiList.false} {ctx.author.mention} Indexes cannot be the same!")

    #     indexFromFake = int(indexFrom)
    #     indexToFake = int(indexTo)

    #     # Get real index 
    #     try:
    #         indexFrom = DBQueue(self.bot.dbConnection).getIndexFromFakeIndex(ctx.guild.id, indexFromFake - 1)
    #         indexTo = DBQueue(self.bot.dbConnection).getIndexFromFakeIndex(ctx.guild.id, indexToFake - 1)
    #     except:
    #         await ctx.send("Problem with getting real Index")

    #     # Get the track to move
    #     try:
    #         trackToMove = DBQueue(self.bot.dbConnection).displaySpecific(ctx.guild.id, indexFrom)
    #         indexFrom = trackToMove[7]
    #     except:
    #         await ctx.send("problem with track move")

    #     # Delete the track to move
    #     try:
    #         DBQueue(self.bot.dbConnection).remove(ctx.guild.id, indexFrom)
    #     except:
    #         await ctx.send("Problem with delete old track")

    #     if indexFrom < indexTo:
    #         # -1 to each track between trackToMove index and 
    #         DBQueue(self.bot.dbConnection).updateRemoveOneToEach(ctx.guild.id, indexFrom, indexTo)
    #     else:
    #         # +1 to each track between trackToMove index and 
    #         DBQueue(self.bot.dbConnection).updateAddOneToEach(ctx.guild.id, indexFrom, indexTo)

    #     # Re-create the track
    #     DBQueue(self.bot.dbConnection).add(trackToMove[0], trackToMove[1], trackToMove[2], trackToMove[3],
    #                                        trackToMove[4], trackToMove[5], trackToMove[6], indexTo)

    #     embed = discord.Embed(title="Song moved",
    #                           description=f"- [**{trackToMove[5]}**]({trackToMove[4]}) was moved from `{indexFromFake}` to `{indexToFake}`.",
    #                           color=discord.Colour.random())
    #     embed.set_footer(text=f"Requested by {ctx.author} | {ctx.message.guild.name}", icon_url=ctx.author.avatar_url)
    #     await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(CogPlaylist(bot))
