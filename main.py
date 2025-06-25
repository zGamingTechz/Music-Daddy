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
4. queue feature -done
5. reset queue on leave
6. skip feature
7. priority based playing? (user priority)
8. search feature -done
'''


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all(), help_command=None)
queue = []
current_song = None
guild_text_channels = {}


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


# Leave in 2 mins if VC empty
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    # If the user left a VC or switched VCs
    if before.channel != after.channel and before.channel is not None:
        vc = before.channel
        bot_in_channel = bot.user in vc.members

        if bot_in_channel:
            await asyncio.sleep(120)  # 2 minute timeout

            # Re-check members after timeout
            vc = before.channel
            members = [m for m in vc.members if not m.bot]

            if len(members) == 0:
                vc_client = discord.utils.get(bot.voice_clients, guild=vc.guild)
                if vc_client and vc_client.channel == vc:
                    text_channel = guild_text_channels.get(vc.guild.id)
                    if text_channel:
                        await text_channel.send("💤 VC was empty for 2 minutes. Daddy left to get milk...")
                        guild_text_channels.pop(vc.guild.id, None)

                    await vc_client.disconnect()


# Commands
# Join command
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        guild_text_channels[ctx.guild.id] = ctx.channel
        await ctx.author.voice.channel.connect()
        await ctx.send("🎧 Daddy has joined your VC!")
    else:
        await ctx.send("You need to be in a voice channel, dumbo.")


# LEave command
@bot.command(aliases=["Leave", "LEAVE", "exit", "Exit"])
async def leave(ctx):
    if ctx.voice_client:
        queue.clear()
        guild_text_channels.pop(ctx.guild.id, None)
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Daddy has left the VC.")
    else:
        await ctx.send("I'm not in a VC, dumbo.")


# Play command
@bot.command()
async def play(ctx, *, query):
    vc = ctx.voice_client
    guild_text_channels[ctx.guild.id] = ctx.channel

    if not vc:
        await join(ctx)
        vc = ctx.voice_client

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

    text_channel = guild_text_channels.get(ctx.guild.id)
    if text_channel:
        await text_channel.send(f"▶️ Now playing: **{title}**")


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


# Skip command
@commands.cooldown(1, 10, commands.BucketType.guild)
@bot.command(aliases=["Skip", "s", "SKIP"])
async def skip(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_connected():
        await ctx.send("I'm not even in a VC, dumbo.")
        return

    if not vc.is_playing():
        await ctx.send("Nothing's playing right now, dumbo.")
        return

    if not queue:
        vc.stop()
        await ctx.send("⏭️ Skipped! The queue is empty...")
        return

    vc.stop()
    await ctx.send("⏭️ Skipped! Playing the next track...")


# Pause command
@bot.command(aliases=["Pause", "PAUSE", "hold", "Hold"])
async def pause(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_connected():
        await ctx.send("I'm not even in a VC, dumbo.")
        return

    if not vc.is_playing():
        await ctx.send("Nothing's playing right now to pause, dumbo.")
        return

    vc.pause()
    await ctx.send("⏸️ Daddy paused the music.")


# Resume command
@bot.command(aliases=["Resume", "RESUME", "continue", "Continue"])
async def resume(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_connected():
        await ctx.send("I'm not even in a VC, dumbo.")
        return

    if not vc.is_paused():
        await ctx.send("Music isn't paused, dumbo.")
        return

    vc.resume()
    await ctx.send("▶️ Daddy resumed the music.")


bot.run(token)