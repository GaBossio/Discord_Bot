import nextcord as discord
from nextcord import Interaction, Member, SlashOption
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio

from keys import TEST_GUILD_ID

class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send('You are not in a voice channel.')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send('I am not in a voice channel.')

    @commands.command()
    async def play(self, ctx, url):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
            return

        channel = ctx.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        voice.play(FFmpegPCMAudio(url))
        await ctx.send(f'Now playing: {url}')

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        # Check if the bot is in a voice channel and if it's the same as the user's channel
        if not voice or not ctx.author.voice or voice.channel != ctx.author.voice.channel:
            await ctx.send("I need to be in the same voice channel as you to pause the music.")
            return

        # Check if the bot is currently playing music
        if voice.is_playing():
            voice.pause()
            await ctx.send("Music paused.")
        else:
            await ctx.send("I am not playing anything.")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('I am not paused.')

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        # Check if the bot is in a voice channel and if it's the same as the user's channel
        if not voice or not ctx.author.voice or voice.channel != ctx.author.voice.channel:
            await ctx.send("I need to be in the same voice channel as you to stop the music.")
            return

        # Check if the bot is currently playing music
        if voice.is_playing():
            voice.stop()
            await ctx.send("Music paused.")
        else:
            await ctx.send("I am not playing anything.")

    @commands.command()
    async def volume(self, ctx, volume: int):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice:
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = volume / 100
            await ctx.send(f"Volume set to {volume}%")
        else:
            await ctx.send("I am not in a voice channel.")


def setup(client):
    client.add_cog(Audio(client))
