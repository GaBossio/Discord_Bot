import nextcord as discord
from nextcord.ext import commands
import os

# Import keys
from keys import DISCORD_TOKEN, OWNER_ID

intents = discord.Intents.default()
intents.message_content = True  # Habilita el intento de contenido de mensajes
bot = commands.Bot(command_prefix='!', owner_id=OWNER_ID, intents=intents)

@bot.event
async def on_ready():
    try:
        await bot.change_presence(activity=discord.Game(name='!help'))
    except Exception as e:
        print(f'Error setting status: {e}')
    print('-------------------------------------------')
    print('Bot is ready.')
    print('-------------------------------------------')


# Comando para apagar el bot (solo el dueño puede usarlo)
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down the bot. Goodbye!")
    await bot.close()

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append(f'cogs.{filename[:-3]}')
        print(f'Loaded cog: {filename[:-3]}')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(DISCORD_TOKEN)