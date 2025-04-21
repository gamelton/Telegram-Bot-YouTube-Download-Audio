# YouTube Audio Telegram Bot

A Telegram bot that downloads audio from YouTube videos and sends them to authorized users.

## Features

- Downloads audio from YouTube videos in MP3 format
- Sends audio files directly to Telegram users
- Restricts access to authorized users only
- Supports both youtube.com and youtu.be URLs

## Requirements

- Python 3.7+
- `python-telegram-bot` library
- `yt-dlp` library
- FFmpeg installed on your system

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/gamelton/Telegram-Bot-YouTube-Download-Audio.git
   cd Telegram-Bot-YouTube-Download-Audio
   ```
2. Install the required Python packages:
   ```
   pip install python-telegram-bot, yt-dlp
3. Install OS packages:
   ```
   apt install ffmpeg
   ```
   
## Configuration

1. Edit the script to add your Telegram Bot token:
   ```
   BOT_TOKEN = "your_bot_token_here"
   ```
2. Add authorized user IDs:
   ```
   ALLOWED_USERS = {
    123456789,  # Replace with actual user IDs
    987654321
   }
   ```

## Usage

1. Start the bot:
   ```
   ./your_bot.py
   ```
2. In Telegram, send these commands to your bot:

   - `/start` - Show welcome message
   - `/help` - Show help information
   - `/downloadyoutubeaudio <url>` - Download audio from YouTube

## Notes

- The bot will automatically delete the downloaded audio files after sending them
- Audio quality is set to best available
- Make sure FFmpeg is installed and accessible at /usr/bin/ffmpeg or update the path in the script
