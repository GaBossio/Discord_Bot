import asyncio
import datetime

import nextcord as discord
from nextcord import SlashOption
from nextcord.ext import commands

from utils_common import get_random_response, get_resource_path, CustomContext
from keys import TEST_GUILD_ID


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(name="mute", description="Crea una votación para silenciar a un miembro",
                           guild_ids=[TEST_GUILD_ID])
    async def mute_poll(self, interaction: discord.Interaction,
                        member: discord.Member = SlashOption(description="Miembro a silenciar", required=True),
                        duration: int = SlashOption(description="Duración de la votación (en segundos)",
                                                    required=False),
                        silenciado: bool = SlashOption(description="Evitar que se reproduzca música", required=False)):
        # Get the voice channel where the user is connected
        user = interaction.user
        voice_channel = user.voice.channel if user.voice else None

        if voice_channel is None:
            await interaction.response.send_message(
                "Primero debe conectase a un salon de auditoria con otros sabios mi señor.",
                ephemeral=True)
            return

        # Count members in the voice channel (excluding bots)
        voice_members = [member for member in voice_channel.members if not member.bot]
        member_count = len(voice_members)

        if member_count < 3:
            await interaction.response.send_message("No hay suficientes sabios del consejo en la sala de reunión.",
                                                    ephemeral=True)
            return

        # Create a poll embed
        embed = discord.Embed(title="Se solicita al Consejo", description=get_random_response("poll_responses", "call"),
                              color=discord.Color.dark_purple())

        image = get_random_response("images", "council")
        thumbnail = get_random_response("images", "member")

        # Prepare the files
        files = [
            discord.File(get_resource_path(thumbnail), filename=thumbnail),
            discord.File(get_resource_path(image), filename=image)
        ]
        embed.set_thumbnail(url=f'attachment://{thumbnail}')
        embed.set_image(url=f'attachment://{image}')

        embed.add_field(name="En esta congregación",
                        value=f"Se pondrá en la balanza el destino de **{member.display_name}**.\nQue los dioses estén de tu lado...",
                        inline=False)

        embed.set_footer(text="✅ para aislar al hereje ❌ para absolverlo de sus pecados", icon_url=member.avatar)
        await interaction.response.send_message(files=files, embed=embed)

        # Fetch the sent message
        poll_message = await interaction.original_message()

        # Add reactions to the poll message
        try:
            await poll_message.add_reaction("✅")
            await poll_message.add_reaction("❌")
        except Exception as e:
            print(f"Error adding reactions: {e}")
            return

        # Check if the bot is muted
        if not silenciado:
            # Get the `play` command from the Music cog
            play_command = self.client.get_command("play_now")
            ctx = CustomContext(interaction)
            if play_command:
                await play_command(ctx, 'Council', 'True')  # Call the play command with context and arguments
            else:
                print("Play command not found.")

        # Check for votes
        def check(reaction, user):
            return user in voice_members and str(reaction.emoji) in ["✅", "❌"]

        yes_votes = 0
        no_votes = 0
        timeout = duration

        required_votes = (member_count + 1) // 2

        try:
            while yes_votes < required_votes and no_votes < required_votes:
                reaction, user = await asyncio.wait_for(self.client.wait_for("reaction_add", check=check),
                                                        timeout=timeout)

                if str(reaction.emoji) == "✅":
                    yes_votes += 1
                elif str(reaction.emoji) == "❌":
                    no_votes += 1
                    print(no_votes)

                if yes_votes >= required_votes:
                    await interaction.followup.send(get_random_response("poll_responses", "mute_yes"))
                    # Timeout the member
                    timeout_duration = datetime.timedelta(minutes=5)  # Timeout duration (e.g., 5 minutes)
                    await member.timeout(timeout_duration)
                    break
                elif no_votes >= required_votes:
                    await interaction.followup.send(get_random_response("poll_responses", "mute_no"))
                    break
        except asyncio.TimeoutError:
            await interaction.followup.send(get_random_response("poll_responses", "mute_neutral"))


def setup(client, db):
    client.add_cog(Poll(client))
