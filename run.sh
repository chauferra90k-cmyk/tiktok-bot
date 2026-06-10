#!/bin/bash

# Quick launcher script for TikTok Bot

echo "🤖 TikTok Bot Launcher"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📝 Please create .env file with your credentials"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the bot
python3 discord_bot.py
