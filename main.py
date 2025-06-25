import discord
from discord.ext import commands
from bot_token import token
import yt_dlp
import asyncio


'''
TO:DO
1. check if already in a vc (say some' like Daddy's busy) -done
2. auto join on play -done
3. auto leave if VC empty for 2 min
4. queue feature
5. reset queue on leave
6. skip feature
7. priority based playing? (user priority)
8. search feature -done
'''


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all(), help_command=None)
queue = []
current_song = None


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
async def play(ctx, *, query):
    vc = ctx.voice_client

    if not vc:
        await join(ctx)
        vc = ctx.voice_client

    if not vc:
        await ctx.send("You must be in a VC, dumbo.")
        return

    is_url = query.startswith("http://") or query.startswith("https://")

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'quiet': True,
        'noplaylist': True
    }

    if not is_url:
        ydl_opts['default_search'] = 'ytsearch'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            info = info['entries'][0]

    song = {
        'url': info['url'],
        'title': info['title']
    }

    # If nothing playing and queue empty → play instantly
    if not vc.is_playing() and not queue:
        queue.append(song)
        await play_next(ctx)
    else:
        queue.append(song)
        await ctx.send(f"➕ Added to queue: **{info['title']}**")


async def play_next(ctx):
    if not queue:
        return

    info = queue.pop(0)

    global current_song
    current_song = info

    stream_url = info['url']
    title = info['title']
    vc = ctx.voice_client

    if not vc:
        return

    def after_play(error):
        if error:
            print(f"❌ Error while playing: {error}")
        fut = asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"❌ Error in after callback: {e}")

    vc.play(
        discord.FFmpegPCMAudio(
            stream_url,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
            options="-vn -loglevel panic"
        ),
        after=after_play
    )
    await ctx.send(f"▶️ Now playing: **{title}**")


# Show queue
@bot.command(name="queue", aliases=["q", "songs"])
async def queue_(ctx):
    if not current_song and not queue:
        await ctx.send("📭 Queue is empty, dumbo.")
        return

    embed = discord.Embed(title="🎶 Music Daddy's Queue", color=discord.Color.purple())

    if current_song:
        embed.add_field(name="▶️ Now Playing", value=f"**{current_song['title']}**", inline=False)

    if queue:
        upcoming = "\n".join([f"{idx + 1}. {song['title']}" for idx, song in enumerate(queue)])
        embed.add_field(name="⏭️ Up Next", value=upcoming, inline=False)

    await ctx.send(embed=embed)


bot.run(token)