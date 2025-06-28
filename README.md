# 🎧 Music Daddy Bot

> A sassy, feature-rich Discord music bot that joins your VC, plays your favorite songs, manages queues, and even leaves when everyone goes AFK — because Daddy doesn’t wait around. 😤

## 🚀 Features

- 🎶 **Play Music**: Search YouTube or provide a URL to play music in VC.
- 🧾 **Queue Management**: Add songs, view what's next, skip or clear the queue.
- ⏸️ **Pause / Resume**: Control the playback with simple commands.
- ⏹️ **Stop**: Stop music and clear the queue.
- ⏭️ **Skip**: Skip the current song with cooldown.
- 💤 **Auto Leave**: Leaves VC after 2 minutes of inactivity.
- 🤖 **Search + Stream**: Uses `yt_dlp` to stream directly from YouTube (no downloading).
- 🗨️ **Fun Messages**: Daddy’s got attitude — expect sass and love.
- 💡 **Custom Help Command**: Shows all commands with stylish embeds.

## ⚙️ Requirements

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to PATH
- Required Python libraries:
```
  pip install -r requirements.txt
```

**requirements.txt**

```
discord.py
yt_dlp
PyNACl
```

## 🔑 Setup

1. Create a file called `bot_token.py` in the project root:

   ```python
   token = "YOUR_DISCORD_BOT_TOKEN"
   ```

2. Run the bot:

   ```bash
   python main.py
   ```

## 🎮 Commands

| Command            | Description                              |
| ------------------ | ---------------------------------------- |
| `&play [song/url]` | Plays a song or adds it to the queue.    |
| `&queue` or `&q`   | Shows the music queue.                   |
| `&pause`           | Pauses the current song.                 |
| `&resume`          | Resumes paused music.                    |
| `&skip`            | Skips the current song.                  |
| `&stop`            | Stops and clears the music queue.        |
| `&join`            | Joins the voice channel.                 |
| `&leave`           | Leaves VC and resets everything.         |
| `&help`            | Displays all commands with descriptions. |

## 📦 To-Do

* [x] Auto VC join on play
* [x] Queue system
* [x] Search & play from query
* [x] Leave VC after inactivity
* [x] Skip command with cooldown
* [ ] Priority-based queue (per-user)
* [ ] Volume control

## 🤝 Contribution

Feel free to fork and submit pull requests. Help Daddy grow stronger. 💪

## 📜 License

This bot is for educational and personal use.

---

👑 *Created with love by Bhavya Soni*

