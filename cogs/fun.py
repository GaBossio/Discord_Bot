import nextcord as discord
from nextcord import Interaction, Member, SlashOption
from nextcord.ext import commands

from keys import TEST_GUILD_ID

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Fun(client))
