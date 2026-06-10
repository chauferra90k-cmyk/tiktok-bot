"""
Discord Bot Interface for TikTok Bot Control
Provides commands to control the TikTok bot via Discord
"""

import discord
from discord.ext import commands
import os
import asyncio
import logging
from dotenv import load_dotenv
from tiktok_bot import TikTokBot, logger

# Load environment variables
load_dotenv()

# Setup Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Global TikTok bot instance
tiktok_bot: TikTokBot = None


@bot.event
async def on_ready():
    """Discord bot ready event"""
    logger.info(f"Discord bot logged in as {bot.user}")
    print(f"✅ Discord Bot Ready: {bot.user}")


@bot.command(name="start")
async def start_bot(ctx):
    """Start the TikTok bot
    Usage: /start
    """
    global tiktok_bot
    
    if tiktok_bot is None:
        await ctx.send("❌ TikTok bot not initialized")
        return
    
    if tiktok_bot.is_running:
        await ctx.send("⚠️ Bot is already running")
        return
    
    try:
        await tiktok_bot.start()
        embed = discord.Embed(
            title="✅ Bot Started",
            description="TikTok bot is now running",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        logger.info("Bot started via Discord command")
    except Exception as e:
        await ctx.send(f"❌ Error starting bot: {str(e)}")
        logger.error(f"Error starting bot: {e}")


@bot.command(name="stop")
async def stop_bot(ctx):
    """Stop the TikTok bot
    Usage: /stop
    """
    global tiktok_bot
    
    if tiktok_bot is None:
        await ctx.send("❌ TikTok bot not initialized")
        return
    
    if not tiktok_bot.is_running:
        await ctx.send("⚠️ Bot is not running")
        return
    
    try:
        await tiktok_bot.stop()
        embed = discord.Embed(
            title="🛑 Bot Stopped",
            description="TikTok bot has been stopped",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        logger.info("Bot stopped via Discord command")
    except Exception as e:
        await ctx.send(f"❌ Error stopping bot: {str(e)}")
        logger.error(f"Error stopping bot: {e}")


@bot.command(name="status")
async def bot_status(ctx):
    """Get bot status
    Usage: /status
    """
    global tiktok_bot
    
    if tiktok_bot is None:
        await ctx.send("❌ TikTok bot not initialized")
        return
    
    try:
        status = await tiktok_bot.get_status()
        
        embed = discord.Embed(
            title="🤖 Bot Status",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Status",
            value="🟢 Running" if status['is_running'] else "🔴 Stopped",
            inline=False
        )
        embed.add_field(
            name="Total Comments",
            value=str(status['total_comments']),
            inline=True
        )
        embed.add_field(
            name="Comments This Hour",
            value=str(status['comments_this_hour']),
            inline=True
        )
        embed.add_field(
            name="Active Hashtags",
            value=f"{len(status['hashtags'])} hashtags",
            inline=True
        )
        embed.add_field(
            name="Comment Templates",
            value=f"{status['comments_count']} templates",
            inline=True
        )
        embed.add_field(
            name="Hashtags",
            value=", ".join(status['hashtags']) or "None",
            inline=False
        )
        
        await ctx.send(embed=embed)
        logger.info("Status command executed")
    except Exception as e:
        await ctx.send(f"❌ Error getting status: {str(e)}")
        logger.error(f"Error getting status: {e}")


@bot.command(name="addhashtag")
async def add_hashtag(ctx, hashtag: str):
    """Add hashtag to target
    Usage: /addhashtag #fyp
    """
    global tiktok_bot
    
    if tiktok_bot is None:
        await ctx.send("❌ TikTok bot not initialized")
        return
    
    if not hashtag.startswith("#"):
        hashtag = "#" + hashtag
    
    try:
        added = tiktok_bot.config_manager.add_hashtag(hashtag)
        
        if added:
            embed = discord.Embed(
                title="✅ Hashtag Added",
                description=f"Added hashtag: {hashtag}",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="⚠️ Hashtag Already Exists",
                description=f"{hashtag} is already in the list",
                color=discord.Color.orange()
            )
        
        await ctx.send(embed=embed)
        logger.info(f"Hashtag added: {hashtag}")
    except Exception as e:
        await ctx.send(f"❌ Error adding hashtag: {str(e)}")
        logger.error(f"Error adding hashtag: {e}")


@bot.command(name="addcomment")
async def add_comment(ctx, *, comment: str):
    """Add comment template
    Usage: /addcomment Amazing content! 🔥
    """
    global tiktok_bot
    
    if tiktok_bot is None:
        await ctx.send("❌ TikTok bot not initialized")
        return
    
    try:
        added = tiktok_bot.config_manager.add_comment(comment)
        
        if added:
            embed = discord.Embed(
                title="✅ Comment Template Added",
                description=f"Added: {comment}",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="⚠️ Comment Already Exists",
                description=f"This comment is already in the list",
                color=discord.Color.orange()
            )
        
        await ctx.send(embed=embed)
        logger.info(f"Comment template added: {comment}")
    except Exception as e:
        await ctx.send(f"❌ Error adding comment: {str(e)}")
        logger.error(f"Error adding comment: {e}")


@bot.command(name="comment")
async def comment_command(ctx, *args):
    """Set hashtags and comment templates
    Usage: /comment #fyp #viral "Amazing!" "Love it!"
    """
    global tiktok_bot
    
    if tiktok_bot is None:
        await ctx.send("❌ TikTok bot not initialized")
        return
    
    if len(args) < 2:
        await ctx.send("❌ Usage: /comment #hashtag1 #hashtag2 \"comment1\" \"comment2\"")
        return
    
    try:
        hashtags = []
        comments = []
        
        for arg in args:
            if arg.startswith("#"):
                hashtags.append(arg)
            else:
                # Remove quotes if present
                clean_arg = arg.strip('"\'')
                if clean_arg:
                    comments.append(clean_arg)
        
        if not hashtags or not comments:
            await ctx.send("❌ Please provide at least one hashtag and one comment")
            return
        
        # Update configuration
        tiktok_bot.config_manager.config["hashtags"] = hashtags
        tiktok_bot.config_manager.config["comments"] = comments
        tiktok_bot.config_manager.save_config()
        
        embed = discord.Embed(
            title="✅ Configuration Updated",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Hashtags",
            value=", ".join(hashtags),
            inline=False
        )
        embed.add_field(
            name="Comment Templates",
            value="\n".join([f"• {c}" for c in comments]),
            inline=False
        )
        
        await ctx.send(embed=embed)
        logger.info(f"Configuration updated: {len(hashtags)} hashtags, {len(comments)} comments")
    except Exception as e:
        await ctx.send(f"❌ Error updating configuration: {str(e)}")
        logger.error(f"Error updating configuration: {e}")


@bot.command(name="help")
async def help_command(ctx):
    """Show help message
    Usage: /help
    """
    embed = discord.Embed(
        title="📚 TikTok Bot Commands",
        description="Control the TikTok bot via Discord",
        color=discord.Color.blue()
    )
    
    commands_list = [
        ("/start", "Start the TikTok bot"),
        ("/stop", "Stop the TikTok bot"),
        ("/status", "Get bot status and statistics"),
        ("/addhashtag <hashtag>", "Add a hashtag to target"),
        ("/addcomment <comment>", "Add a comment template"),
        ("/comment <hashtags> <comments>", "Set hashtags and comments"),
        ("/help", "Show this help message"),
    ]
    
    for cmd, description in commands_list:
        embed.add_field(name=cmd, value=description, inline=False)
    
    await ctx.send(embed=embed)


async def main():
    """Main function to run the bot"""
    global tiktok_bot
    
    # Get credentials from environment
    discord_token = os.getenv("DISCORD_TOKEN")
    tiktok_username = os.getenv("TIKTOK_USERNAME")
    tiktok_password = os.getenv("TIKTOK_PASSWORD")
    
    if not discord_token:
        logger.error("DISCORD_TOKEN not found in .env")
        return
    
    if not tiktok_username or not tiktok_password:
        logger.error("TikTok credentials not found in .env")
        return
    
    # Initialize TikTok bot
    tiktok_bot = TikTokBot(tiktok_username, tiktok_password)
    
    try:
        if not await tiktok_bot.initialize():
            logger.error("Failed to initialize TikTok bot")
            return
        
        # Run Discord bot
        async with bot:
            await bot.start(discord_token)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    
    finally:
        if tiktok_bot:
            await tiktok_bot.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
