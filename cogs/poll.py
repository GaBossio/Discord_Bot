import nextcord as discord
from nextcord.ext import commands

import asyncio

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

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

        # Add reactions for voting
        await message.add_reaction('👍')
        await message.add_reaction('👎')

        # Count the members in the voice channel
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            total_members = len(voice_channel.members)
            required_votes = total_members // 2  # Calculate half of the voice channel members
        else:
            await ctx.send('You are not in a voice channel, so the poll will run without a user count.')
            total_members = 0
            required_votes = 0

        # Dictionary to keep track of votes
        votes = {'👍': 0, '👎': 0}

        # Wait for votes for 1 minute or until half have voted
        timeout = 60
        end_poll = False

        while not end_poll:
            try:
                # Wait for a reaction
                reaction, user = await self.client.wait_for(
                    'reaction_add',
                    timeout=timeout,
                    check=lambda r, u: u != self.client.user and r.message.id == message.id
                )
                if str(reaction.emoji) in votes:
                    votes[str(reaction.emoji)] += 1

                # Check if half of the voice channel members have voted
                if total_members > 0 and votes[str(reaction.emoji)] >= required_votes:
                    end_poll = True

            except asyncio.TimeoutError:
                # If the timeout is reached, end the poll
                end_poll = True

        # Count the votes
        thumbs_up = votes['👍']
        thumbs_down = votes['👎']

        # Create results embed
        results_embed = discord.Embed(
            title='Poll Results',
            description=f'**{question}**\n👍: {thumbs_up} votes\n👎: {thumbs_down} votes',
            color=discord.Color.green()
        )

        # Send results
        await ctx.send(embed=results_embed)

async def setup(bot):
    bot.add_cog(Poll(bot))