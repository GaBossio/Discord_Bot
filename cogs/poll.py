import nextcord as discord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import asyncio
from keys import TEST_GUILD_ID

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(name="yesnopoll", description="Create a Yes or No poll", guild_ids=[TEST_GUILD_ID])
    async def yes_no_poll(self, interaction: discord.Interaction, question: str):
        # Create a poll embed
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
        embed.add_field(name="Options", value="✅ Yes\n❌ No", inline=False)
        await interaction.response.send_message(embed=embed)

        # Fetch the sent message
        poll_message = await interaction.original_message()  # Get the original response message
        print(poll_message.id)

        # Add reactions to the poll message
        try:
            await poll_message.add_reaction("✅")
            await poll_message.add_reaction("❌")
        except Exception as e:
            print(f"Error adding reactions: {e}")

    @commands.command()
    async def poll(self, ctx, *, question: str):
        """Creates a poll with a question and counts votes after 1 minute, ending early if half of voice chat votes"""
        embed = discord.Embed(
            title=question,
            description='React with 👍 or 👎',
            color=discord.Color.blue()
        )

        # Send the embed message
        message = await ctx.send(embed=embed)

        # Add reactions for voting with error handling
        try:
            await message.add_reaction('👍')
            await asyncio.sleep(1)  # Wait for a second to avoid rate limits
            await message.add_reaction('👎')
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")


def setup(client):
    client.add_cog(Poll(client))
