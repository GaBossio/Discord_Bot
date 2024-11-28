import nextcord as discord
from nextcord import Interaction, Member, SlashOption, FFmpegPCMAudio
from nextcord.ext import commands

from keys import TEST_GUILD_ID


class Test(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db

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
    async def test(self, interaction: Interaction,
                   member: Member = SlashOption(description="Select a member", required=False),
                   option1: str = SlashOption(description="First option", required=False,
                                              choices=['Option 1', 'Option 2']),
                   ):
        await interaction.response.send_message(f'Test command working! Member: {member.name}', ephemeral=True)

        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('resources/Council.mp3')
            player = voice.play(source)
        else:
            await interaction.send('You are not in a voice channel.')

    # @commands.command()
    # async def test(self, ctx):
    #     # Create the initial button
    #     button = discord.ui.Button(label="Click me!", style=discord.ButtonStyle.primary)
    #
    #     # Define the interaction callback
    #     async def button_callback(interaction: discord.Interaction):
    #         # Create a new button instance for the view
    #         new_button = discord.ui.Button(label="Clicked!", style=discord.ButtonStyle.secondary, disabled=True)
    #
    #         # Create a new view and add the disabled button
    #         new_view = discord.ui.View()
    #         new_view.add_item(new_button)
    #
    #         # Update the message to reflect the new button state
    #         await interaction.message.edit(view=new_view)
    #
    #         # Send an ephemeral response to the user who clicked the button
    #         await interaction.response.send_message("Button disabled for you!", ephemeral=True)
    #
    #     # Attach the callback to the original button
    #     button.callback = button_callback
    #
    #     # Create a view to hold the button
    #     view = discord.ui.View()
    #     view.add_item(button)
    #
    #     # Send the message with the button
    #     await ctx.send("Here is a button:", view=view)

    @commands.command()
    async def test(self, ctx):
        doc_ref = self.db.collection("guilds").document(f"Guild ID")
        doc = doc_ref.get()
        if doc.exists:
            print("Document data:", doc.to_dict())
        else:
            print("No such document!")

            


def setup(client, db):
    client.add_cog(Test(client, db))
