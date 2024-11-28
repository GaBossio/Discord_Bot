import nextcord as discord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from keys import TEST_GUILD_ID


class Common(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db

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

    @commands.command()
    async def get_config(self, ctx):
        # Fetch the guild configuration
        config = self.db.fetch_guild(ctx.guild.id)

        if config:
            # Display the configuration in a formatted embed
            embed = discord.Embed(
                title=f"Configuration for {ctx.guild.name}",
                color=discord.Color.blue()
            )
            for key, value in config.items():
                embed.add_field(name=key.capitalize(), value=value, inline=False)

            await ctx.send(embed=embed)
        else:
            # Display an error message if no configuration is found
            await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="No configuration found for this guild. Creating a new one...",
                    color=discord.Color.red()
                )
            )
            self.db.create_guild(ctx.guild.id)
            await ctx.send("Configuration created successfully.")


def setup(client, db):
    client.add_cog(Common(client, db))
