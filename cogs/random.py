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
        name='roll_dice',
        description='Roll a dice. Default is 20-sided.',
        guild_ids=[TEST_GUILD_ID]
    )
    async def roll_dice(
            self,
            interaction: Interaction,
            max_number: int = SlashOption(
                description="The maximum number for the dice (e.g., 6 for 6-sided, 2 for coin toss)", required=False,
                default=20)
    ):
        # Ensure the max number is at least 2
        if max_number < 2:
            await interaction.response.send_message("The dice must have at least 2 sides!", ephemeral=True)
            return

        # Roll the dice
        result = random.randint(1, max_number)
        await interaction.response.send_message(f"You rolled a {result} (1-{max_number})", ephemeral=False)

    @discord.slash_command(
        name='pick_random',
        description='Randomly pick a member from the current voice channel.',
        guild_ids=[TEST_GUILD_ID]
    )
    async def pick_random(
            self,
            interaction: Interaction,
            exclude_members: str = SlashOption(description="Mention members to exclude (e.g., @user1 @user2)",
                                               required=False),
    ):
        # Check if the user is in a voice channel
        voice_state = interaction.user.voice
        if not voice_state or not voice_state.channel:
            await interaction.response.send_message("You are not in a voice channel!", ephemeral=True)
            return

        voice_channel = voice_state.channel
        members_in_channel = voice_channel.members

        # Parse excluded member mentions into a list of IDs
        exclude_list = []
        if exclude_members:
            # Extract mentions from the exclude_members string
            exclude_list = [int(user[2:-1]) for user in exclude_members.split() if
                            user.startswith('<@') and user.endswith('>')]

        # Filter out excluded members and bots
        eligible_members = [
            member for member in members_in_channel
            if member.id not in exclude_list and not member.bot  # Exclude specified member and bots
        ]

        if not eligible_members:
            await interaction.response.send_message("There are no eligible members to select.", ephemeral=True)
            return

        # Randomly select a member
        selected_member = random.choice(eligible_members)

        await interaction.response.send_message(f"{selected_member.mention} has been selected!", ephemeral=False)


def setup(client):
    client.add_cog(Random(client))
