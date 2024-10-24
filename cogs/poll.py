import asyncio
import datetime
import json
import os
import random

import nextcord as discord
from nextcord import Interaction, Member, SlashOption
from nextcord.ext import commands

from keys import TEST_GUILD_ID


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(name="mute", description="Create a Yes or No poll", guild_ids=[TEST_GUILD_ID])
    async def yes_no_poll(self, interaction: discord.Interaction, member: discord.Member, duration: int = 60):
        # Get the voice channel where the user is connected
        user = interaction.user
        voice_channel = user.voice.channel if user.voice else None

        if voice_channel is None:
            await interaction.response.send_message("Primero debe conectase a un salon de auditoria con otros sabios mi señor.",
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
        embed = discord.Embed(title="Se solicita al Consejo", description=self.get_random_response("call"),
                              color=discord.Color.dark_purple())
        #embed.set_author(name=member.display_name, icon_url=member.avatar)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Prepare the files
        files = [
            discord.File(os.path.join(base_dir, "resources", "consejo1.png"), filename='consejo1.png'),
            discord.File(os.path.join(base_dir, "resources", "call1.png"), filename='call1.png')
        ]
        embed.set_thumbnail(url='attachment://consejo1.png')
        embed.set_image(url='attachment://call1.png')

        embed.add_field(name="En esta congregación", value=f"Se pondrá en la balanza el destino de **{member.display_name}**.\nQue los dioses estén de tu lado...",
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

        # Check for votes
        def check(reaction, user):
            return user in voice_members and str(reaction.emoji) in ["✅", "❌"]

        yes_votes = 0
        no_votes = 0
        timeout = duration

        required_votes = (member_count+1) // 2

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
                    await interaction.followup.send(self.get_random_response("mute_yes"))
                    # Timeout the member
                    timeout_duration = datetime.timedelta(minutes=5)  # Timeout duration (e.g., 5 minutes)
                    await member.timeout(timeout_duration)
                    break
                elif no_votes >= required_votes:
                    await interaction.followup.send(self.get_random_response("mute_no"))
                    break
        except asyncio.TimeoutError:
            await interaction.followup.send(self.get_random_response("mute_neutral"))

    def get_random_response(self, category):
        # Construct the path to the 'resources.json' file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "resources", "responses.json")

        try:
            # Specify UTF-8 encoding while opening the file
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return random.choice(data["poll_responses"][category])
        except (FileNotFoundError, KeyError) as e:
            return f"Error: {e}"
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"



    @discord.slash_command(
            name='poll',
            description='Create a poll with up to 5 options. Defaults to a Yes/No poll if no options are provided.',
            guild_ids=[TEST_GUILD_ID]
    )
    async def poll(
            self,
            interaction: Interaction,
            question: str = SlashOption(description="The poll question", required=True),
            option1: str = SlashOption(description="First option (default: Yes)", required=False),
            option2: str = SlashOption(description="Second option (default: No)", required=False),
            option3: str = SlashOption(description="Third option", required=False),
            option4: str = SlashOption(description="Fourth option", required=False),
            option5: str = SlashOption(description="Fifth option", required=False)
        ):

            # Collect the options into a list, filtering out None values (unused options)
            options = [option for option in [option1, option2, option3, option4, option5] if option]

            # If no options are provided, default to a Yes/No poll
            if not options:
                # Create an embed for the poll
                embed = discord.Embed(
                    title="Encuesta",
                    description=question,
                    color=discord.Color.blue()
                )
                # Send the poll as an embed
                poll_message = await interaction.channel.send(embed=embed)
                await poll_message.add_reaction("✅")
                await poll_message.add_reaction("❌")
                return

            # List of reactions to use for the poll
            reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]  # Emoji reactions for up to 5 options

            # Create an embed for the poll
            embed = discord.Embed(
                title="Encuesta",
                description=question,
                color=discord.Color.blue()
            )


            for i, option in enumerate(options):
                embed.add_field(name=f"", value=f"{reactions[i]} {option}", inline=False)

            # Send the poll as an embed
            poll_message = await interaction.channel.send(embed=embed)

            # Add reactions to the poll message for voting
            for i in range(len(options)):
                await poll_message.add_reaction(reactions[i])

            print("DEBUG: Poll created successfully")


def setup(client):
    client.add_cog(Poll(client))
