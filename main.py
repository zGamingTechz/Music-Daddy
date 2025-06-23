import discord
from discord.ext import commands
from bot_token import token


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all(), help_command=None)


# Login Status & On Ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("&help"))
    print(f"We Have Logged In As {bot.user}")


bot.run(token)