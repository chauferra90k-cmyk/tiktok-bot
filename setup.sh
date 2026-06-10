#!/bin/bash

# TikTok Bot Installation Script for Termux/Linux

echo "🚀 TikTok Bot - Installation Script"
echo "===================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Update pip
echo "📦 Updating pip..."
python3 -m pip install --upgrade pip

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers (optional, for web automation)
echo "📦 Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your credentials!"
    echo "   nano .env"
fi

echo ""
echo "✅ Installation completed!"
echo "===================================="
echo "📝 Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python3 discord_bot.py"
echo ""
