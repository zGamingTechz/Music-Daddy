import discord
from discord.ext import commands
from bot_token import token
import yt_dlp


'''
TO:DO
1. check if already in a vc (say some' like Daddy's busy)
2. auto join on play
3. auto leave if VC empty for 2 min
4. queue feature
5. reset queue on leave
6. skip feature
7. priority based playing? (user priority)
'''


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


# Play command
@bot.command()
async def play(ctx, url):
    vc = ctx.voice_client

    if not vc:
        await join(ctx)
        vc = ctx.voice_client

    # If user not in VC and bot also isn't, bail out
    if not vc:
        await ctx.send("You must be in a VC, dumbo.")
        return

    # Check if already playing something
    if vc.is_playing():
        await ctx.send("Daddy's busy playing something already 🎶")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info['url']

    vc.play(discord.FFmpegPCMAudio(stream_url))
    await ctx.send(f"▶️ Now playing: **{info['title']}**")


bot.run(token)