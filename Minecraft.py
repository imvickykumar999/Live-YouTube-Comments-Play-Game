import discord
import asyncio
import threading
import os
import time
from pynput.keyboard import Controller
from dotenv import load_dotenv

# Load Discord bot token from environment variables
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  

if not BOT_TOKEN:
    raise ValueError("❌ ERROR: Discord bot token is missing!")

# Initialize keyboard controller
keyboard = Controller()

# Movement flags
moving_forward = False

# Initialize Discord Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  

# Initialize Discord Client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    global moving_forward
    
    if message.author == client.user:
        return  # Ignore bot's own messages
    
    content = message.content.lower().strip()
    
    print(f"📩 {message.author} said: {content}")

    # Movement logic
    if content == "w":
        if not moving_forward:
            keyboard.press('w')
            moving_forward = True
            print("🚀 Moving forward...")
    elif content == "s":
        if moving_forward:
            keyboard.release('w')
            moving_forward = False
            print("⏹ Stopped moving forward.")
        keyboard.release('a')
        keyboard.release('d')
    elif content == "a":
        keyboard.press('a')
        time.sleep(0.1)
        keyboard.release('a')
        print("↩ Turning left...")
    elif content == "d":
        keyboard.press('d')
        time.sleep(0.1)
        keyboard.release('d')
        print("↪ Turning right...")

# Function to start the bot
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client.run(BOT_TOKEN)

# Start bot in a new thread
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

# Keep script running
while True:
    pass  # Prevents script from exiting
