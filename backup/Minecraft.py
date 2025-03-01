from googleapiclient.discovery import build
from pynput.keyboard import Controller, Key
import time

# Initialize keyboard controller
keyboard = Controller()

# YouTube API setup
API_KEY = 'YOUR API KEY'  # Replace with your API key
VIDEO_ID = input('Enter Live YouTube Video ID : ')  # Replace with your live video ID

# Global flags
moving_forward = False

# Start moving forward (press 'W')
def start_moving_forward():
    global moving_forward
    if not moving_forward:
        keyboard.press('w')
        moving_forward = True
        print("Moving forward...")

# Stop all movement
def stop_movement():
    global moving_forward
    if moving_forward:
        keyboard.release('w')
        moving_forward = False
        print("Stopped moving forward.")
    keyboard.release('a')
    keyboard.release('d')
    print("Stopped all actions.")

# Turn left ('A') or right ('D')
def turn(direction):
    if direction == 'left':
        keyboard.press('a')
        time.sleep(0.1)
        keyboard.release('a')
        print("Turning left...")
    elif direction == 'right':
        keyboard.press('d')
        time.sleep(0.1)
        keyboard.release('d')
        print("Turning right...")

# Process comments and map them to actions
def process_comment(comment):
    normalized_comment = comment.lower().strip()
    # if normalized_comment == 'jump':
    #     keyboard.press(Key.space)
    #     time.sleep(0.1)
    #     keyboard.release(Key.space)
    if normalized_comment == 'w':
        start_moving_forward()
    elif normalized_comment == 'a':
        turn('left')
    elif normalized_comment == 'd':
        turn('right')
    elif normalized_comment == 's':
        stop_movement()

# Fetch live chat messages
def fetch_live_chat(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Get live chat ID
    video_response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()

    if 'items' not in video_response or not video_response['items']:
        print("No live video found with the provided ID.")
        return

    live_chat_id = video_response['items'][0].get('liveStreamingDetails', {}).get('activeLiveChatId')
    if not live_chat_id:
        print("Live chat not available for this video.")
        return

    print("Fetching live chat messages...")
    while True:
        chat_response = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part='snippet'
        ).execute()

        # Process each message
        for item in chat_response.get('items', []):
            message = item['snippet']['displayMessage']
            print(f"Received comment: {message}")
            process_comment(message)

        # Pause before fetching again to respect API rate limits
        time.sleep(3)

# Main execution
try:
    print("Starting script. Press Ctrl+C to stop.")
    fetch_live_chat(VIDEO_ID)
except KeyboardInterrupt:
    stop_movement()
    print("\nScript stopped.")

# https://www.youtube.com/live_chat?is_popout=1&v=Mvr4NQF0IuQ
