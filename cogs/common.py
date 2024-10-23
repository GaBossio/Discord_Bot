import nextcord as discord
from nextcord.ext import commands

class Common(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f'Welcome {member.mention}!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

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
    async def count_members(self, ctx):
        # Check if the author is in a voice channel
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            # Count the number of members in the voice channel
            member_count = len(voice_channel.members)
            await ctx.send(f'There are {member_count} members in {voice_channel.name}.')
        else:
            await ctx.send('You are not in a voice channel.')

def setup(client):
    client.add_cog(Common(client))