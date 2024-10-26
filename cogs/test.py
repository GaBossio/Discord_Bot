import nextcord as discord
from nextcord import FFmpegPCMAudio
from nextcord import Interaction, Member, SlashOption
from nextcord.ext import commands

from common_utils import get_random_response
from keys import TEST_GUILD_ID


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            print('Bot message: ' + ctx.content)
        else:
            print(f'User {ctx.author.name} message: {ctx.content}')

    @discord.slash_command(
        name='test',
        description='Test command',
        guild_ids=[TEST_GUILD_ID]
    )
    async def test(self, interaction: Interaction,
                   member: Member = SlashOption(description="Select a member", required=False),
                   option1: str = SlashOption(description="First option", required=False,
                                              choices=['Option 1', 'Option 2']),
                   ):
        await interaction.response.send_message(f'Test command working! Member: {member.name}', ephemeral=True)

        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('resources/Counsil.mp3')
            player = voice.play(source)
        else:
            await interaction.send('You are not in a voice channel.')

    @commands.command()
    async def test(self, ctx, category: str, subcategory: str):
        response = get_random_response(category, subcategory)
        await ctx.send(response)


def setup(client):
    client.add_cog(Test(client))
