import nextcord as discord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from keys import TEST_GUILD_ID


class Common(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    @discord.slash_command(
        name='clear',
        description="Elimina mensajes en el canal actual",
        guild_ids=[TEST_GUILD_ID]
    )
    async def clear(
            self,
            interaction: Interaction,
            cantidad: int = SlashOption(description="Cantidad de mensajes a eliminar", required=True),
            miembro: discord.Member = SlashOption(description="Solo eliminar mensajes de este usuario", required=False)
    ):
        def check(message):
            return not miembro or message.author == miembro

        deleted = await interaction.channel.purge(limit=cantidad, check=check)

        await interaction.response.send_message(f"Se eliminaron {len(deleted)} mensajes.", ephemeral=True)


def setup(client, db):
    client.add_cog(Common(client))
