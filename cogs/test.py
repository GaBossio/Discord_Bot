import nextcord as discord
from nextcord import Interaction, Member, SlashOption
from nextcord.ext import commands

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
    async def test(self, interaction: Interaction, member: Member = SlashOption(description="Select a member")):
        await interaction.response.send_message(f'Test command working! Member: {member.name}', ephemeral=True)


def setup(client):
    client.add_cog(Test(client))
