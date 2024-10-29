import os

import nextcord as discord
from nextcord import ActivityType
from nextcord.ext import commands

from utils_db import Database
# Import keys
from keys import DISCORD_TOKEN, OWNER_ID

# Setup intents
intents = discord.Intents.all()

# Create the bot instance
bot = commands.Bot(command_prefix='!', owner_id=OWNER_ID, intents=intents)

# Create an instance of the Database
db = Database()


@bot.event
async def on_ready():
    try:
        activity = discord.Activity(type=ActivityType.listening, name="las órdenes del consejo")
        await bot.change_presence(status=discord.Status.online, activity=activity)
        db.connect()
    except Exception as e:
        print(f'Error setting status: {e}')
    print('-------------------------------------------')
    print('Bot is ready.')
    print('-------------------------------------------')


# Command to shutdown the bot (only the owner can use it)
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await db.disconnect()
    await ctx.send("Shutting down the bot. Goodbye!")
    await bot.close()


# Load cogs
if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # Import the cog module dynamically
            module_name = f'cogs.{filename[:-3]}'
            cog = __import__(module_name, fromlist=['setup'])
            # Call the setup function with the bot and db instances
            cog.setup(bot, db)
            print(f'Loaded cog: {filename[:-3]}')

# Run the bot
bot.run(DISCORD_TOKEN)
