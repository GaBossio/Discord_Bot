import builtins

import nextcord as discord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

random = builtins.__import__('random')

from keys import TEST_GUILD_ID


class Random(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(
        name='dado',
        description='Tira un dado, el predeterminado es de 20-caras.',
        guild_ids=[TEST_GUILD_ID]
    )
    async def roll_dice(
            self,
            interaction: Interaction,
            max_number: int = SlashOption(
                description="El número de caras del dado (6 para un dado normal, 2 para tirar una moneda).", required=False,
                default=20)
    ):
        # Ensure the max number is at least 2
        if max_number < 2:
            await interaction.response.send_message("El dado debe tener al menos 2 caras!", ephemeral=True)
            return

        # Roll the dice
        result = random.randint(1, max_number)
        await interaction.response.send_message(f"Sacaste un {result} (1-{max_number})", ephemeral=False)

    @discord.slash_command(
        name='elegir',
        description='Elige un miembro aleatorio de tu canal de voz.',
        guild_ids=[TEST_GUILD_ID]
    )
    async def pick_random(
            self,
            interaction: Interaction,
            excluir: str = SlashOption(description="Menciona a los miembros que no quieres que sean elegidos.",
                                               required=False),
    ):
        # Check if the user is in a voice channel
        voice_state = interaction.user.voice
        if not voice_state or not voice_state.channel:
            await interaction.response.send_message("No estas en un canal de voz!", ephemeral=True)
            return

        voice_channel = voice_state.channel
        members_in_channel = voice_channel.members

        # Parse excluded member mentions into a list of IDs
        exclude_list = []
        if excluir:
            # Extract mentions from the exclude_members string
            exclude_list = [int(user[2:-1]) for user in excluir.split() if
                            user.startswith('<@') and user.endswith('>')]

        # Filter out excluded members and bots
        eligible_members = [
            member for member in members_in_channel
            if member.id not in exclude_list and not member.bot  # Exclude specified member and bots
        ]

        if not eligible_members:
            await interaction.response.send_message("No hay miembros elegibles para la selección", ephemeral=True)
            return

        # Randomly select a member
        selected_member = random.choice(eligible_members)

        await interaction.response.send_message(f"{selected_member.mention} ha sido seleccionado!", ephemeral=False)


def setup(client, db):
    client.add_cog(Random(client))
