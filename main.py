import discord
from discord.ext import commands
from bot_token import token


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all(), help_command=None)


# Login Status & On Ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("&help"))
    print(f"We Have Logged In As {bot.user}")


@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await message.channel.send("Hello?")

    await bot.process_commands(message)


# Commands
# Join command
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("🎧 Daddy has joined your VC!")
    else:
        await ctx.send("You need to be in a voice channel, dumbo.")


# LEave command
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Daddy has left the VC.")
    else:
        await ctx.send("I'm not in a VC, dumbo.")


bot.run(token)