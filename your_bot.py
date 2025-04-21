#!/usr/bin/env python3

# Telegram Bot for downloading YouTube audio.

# Requirements:
## Telegram Bot API Server: https://github.com/tdlib/telegram-bot-api/
## System packages: ffmpeg
## Python packages: python-telegram-bot, yt-dlp

import logging
import os
from pathlib import Path
from typing import Optional

import yt_dlp
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# List of allowed user IDs (replace with your actual allowed users)
ALLOWED_USERS = {
    123807789,  # Example user ID 1
    000000000   # Example user ID 2
}
BOT_TOKEN = "token"
FFMPEG_PATH = "/usr/bin/ffmpeg"  # Default ffmpeg path on Ubuntu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id if user else None
    
    try:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Your user ID is: {user_id}. I'm a bot running in {'local' if LOCAL_MODE else 'normal'} mode.  \n"
            "Available commands:\n"
            "/start - Show this message\n"
            "/help - Show help information\n"
            "/downloadyoutubeaudio url - Download audio from YouTube"
        )
    except Exception as e:
        logger.error(f"Cannot send start message: {e}")
        await update.message.reply_text(f"Sorry, I couldn't send the welcome message: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help information."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Show welcome message\n"
        "/help - Show this help\n"
        "/downloadyoutubeaudio <url> - Download audio from YouTube\n\n"
        "Example:\n"
        "/downloadyoutubeaudio https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

async def downloadyoutubeaudio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    # Check if user is allowed
    if not user or user.id not in ALLOWED_USERS:
        await update.message.reply_text(
            chat_id=update.effective_chat.id,
            text="?? Sorry, you don't have permission to use this command."
        )
        return
    
    url = update.message.text.split()[1] if update.message.text else None  # Assuming the URL is sent as a message
    # Validate URL
    if 'youtube.com' not in url and 'youtu.be' not in url:
        await update.message.reply_text("Please provide a valid YouTube URL.")
        return
    
    # Set up yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',  # Best quality
        }],
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Default ffmpeg path on Ubuntu
        'outtmpl': '%(title)s.%(ext)s',
        'download_archive': None,  # Don't record downloaded videos
        'external_downloader_args': {
            'ffmpeg_i': ['-reconnect', '1', '-reconnect_streamed', '1', '-reconnect_delay_max', '5']
        }
    }
    
    try:
        # Send "processing" message
        processing_msg = await update.message.reply_text("Downloading audio...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # The actual file will have the mp3 extension
            mp3_filename = os.path.splitext(filename)[0] + '.mp3'
            
            if mp3_filename:
                # Send the audio file
                with open(mp3_filename, 'rb') as audio_file:
                    await update.message.reply_audio(
                        audio=audio_file,
                        title=info.get('title', 'audio'),
                        performer=info.get('uploader', 'unknown artist'),
                        duration=info.get('duration', 0)
                    )
                
                # Delete the temporary file
                os.remove(mp3_filename)
                
                # Update processing message
                await processing_msg.edit_text("Audio sent successfully!")
    
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await update.message.reply_text(f"Sorry, I couldn't download that video. Error: {e}")
        
        # If processing message exists, update it with error
        if 'processing_msg' in locals():
            await processing_msg.edit_text(f"Sorry, I couldn't download that video. Error: {e}"
            )

if __name__ == '__main__':
    """Start the bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).base_url("http://localhost:8081/bot").build()
    
    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("downloadyoutubeaudio", downloadyoutubeaudio))
    
    logger.info("Bot is starting...")
    application.run_polling()
