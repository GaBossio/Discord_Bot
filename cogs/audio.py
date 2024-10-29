import nextcord as discord
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio

class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = {}

    def check_queue(self, ctx):
        guild_id = ctx.guild.id
        if self.queue.get(guild_id):
            voice = ctx.guild.voice_client
            if voice and not voice.is_playing():
                source = self.queue[guild_id].pop(0)
                voice.play(source, after=lambda x=None: self.check_queue(ctx))

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if not ctx.voice_client:
                await channel.connect()
            else:
                await ctx.voice_client.move_to(channel)
        else:
            await ctx.send('You are not in a voice channel.')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            guild_id = ctx.guild.id
            self.queue[guild_id] = []
        else:
            await ctx.send('I am not in a voice channel.')

    @commands.command()
    async def play(self, ctx, arg, silent: bool = False):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if not ctx.author.voice:
            if not silent:
                await ctx.send("You are not in a voice channel.", ephemeral=True)
            return

        channel = ctx.author.voice.channel
        if not voice:
            voice = await channel.connect()

        song = 'resources/' + arg + '.mp3'
        source = FFmpegPCMAudio(song)
        guild_id = ctx.guild.id

        if voice.is_playing():
            self.queue.setdefault(guild_id, []).append(source)
            if not silent:
                await ctx.send(f'{arg} added to queue.')
        else:
            voice.play(source, after=lambda x=None: self.check_queue(ctx))
            if not silent:
                await ctx.send(f'Now playing: {song}')

    @commands.command()
    async def play_now(self, ctx, arg, silent: bool = False):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not ctx.author.voice:
            if not silent:
                await ctx.send("You are not in a voice channel.", ephemeral=True)
            return

        channel = ctx.author.voice.channel
        if not voice:
            voice = await channel.connect()
        song = 'resources/' + arg + '.mp3'
        source = FFmpegPCMAudio(song)
        guild_id = ctx.guild.id

        # Si se está reproduciendo, pausa el audio actual
        if voice.is_playing():
            # Guardar el audio actual
            current_source = voice.source
            voice.pause()  # Pausar el audio actual

            # Reproduce el nuevo audio inmediatamente
            voice.play(source, after=lambda x=None: self.resume(ctx, current_source))
            if not silent:
                await ctx.send(f'Now playing immediately: {song}')
        else:
            # Si no hay nada reproduciéndose, simplemente reproduce el audio
            voice.play(source, after=lambda x=None: self.check_queue(ctx))
            if not silent:
                await ctx.send(f'Now playing: {song}')

    @commands.command()
    async def skip(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Skipped current song.")
            self.check_queue(ctx)
        else:
            await ctx.send("I am not playing anything.")

    @commands.command()
    async def clear(self, ctx):
        guild_id = ctx.guild.id
        if guild_id in self.queue:
            self.queue[guild_id] = []
            await ctx.send("Queue cleared.")
        else:
            await ctx.send("The queue is already empty.")

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Music paused.")
        else:
            await ctx.send("I am not playing anything.")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Music resumed.")
        else:
            await ctx.send("I am not paused.")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Music stopped.")
        else:
            await ctx.send("I am not playing anything.")

    @commands.command()
    async def queue(self, ctx, arg):
        song = 'resources/' + arg + '.mp3'
        source = FFmpegPCMAudio(song)
        guild_id = ctx.guild.id
        self.queue.setdefault(guild_id, []).append(source)
        await ctx.send(f'{arg} added to queue.')

    @commands.command()
    async def volume(self, ctx, volume: int):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.source:
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = volume / 100
            await ctx.send(f"Volume set to {volume}%")
        else:
            await ctx.send("I am not in a voice channel or playing audio.")


def setup(client, db):
    client.add_cog(Audio(client))
