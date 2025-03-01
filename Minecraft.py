import discord
import asyncio
import threading
import os
import time
import re
from dotenv import load_dotenv
from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController, Button  # Correct import

# Load environment variables
load_dotenv()

# Get Discord bot token
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  

if not BOT_TOKEN:
    raise ValueError("❌ ERROR: Discord bot token is missing!")

# Initialize controllers
keyboard = Controller()
mouse = MouseController()

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
    elif content == "jump":
        keyboard.press(Key.space)
        time.sleep(0.1)
        keyboard.release(Key.space)
        print("🦘 Jumping...")
    elif content == "dig":
        mouse.press(Button.left)
        time.sleep(5)  # Hold left click for 0.5 seconds
        mouse.release(Button.left)
        print("⛏️ Digging...")

    # Handle turning with angles
    match = re.match(r"turn (left|right) (\d+)", content)
    if match:
        direction, angle = match.groups()
        angle = int(angle)

        if direction == "left":
            keyboard.press('a')
        else:
            keyboard.press('d')

        time.sleep(angle / 100)  # Adjust turning time based on angle
        keyboard.release('a' if direction == "left" else 'd')
        print(f"🔄 Turning {direction} by {angle} degrees...")

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
