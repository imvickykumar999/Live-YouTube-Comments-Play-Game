from googleapiclient.discovery import build
from pynput.keyboard import Controller, Key
import time

# Initialize the keyboard controller
keyboard = Controller()

# Define a function to press a key based on the comment
def press_key(comment):
    key_map = {
        'w': 'w',
        'a': 'a',
        's': 's',
        'd': 'd',
        'jump': Key.space
    }
    # Normalize the comment text
    normalized_comment = comment.lower().strip()
    # Check if the comment matches any mapped key
    if normalized_comment in key_map:
        key = key_map[normalized_comment]

        keyboard.press(key)
        time.sleep(1)
        keyboard.release(key)
        print(f"Pressed key: {key}")

def get_live_chat_messages(video_id):
    youtube = build('youtube', 'v3', developerKey='AIzaSyCcJX4qdbo9caqxZSKDmuBjNVWfvq8_Wcs')

    # Get the live chat ID
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

    # Fetch live chat messages in a loop
    print("Fetching live chat messages...")
    while True:
        chat_response = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part='snippet,authorDetails'
        ).execute()

        # Ensure there are items in the response
        if 'items' in chat_response and chat_response['items']:
            # Get the last message from the chat
            last_message = chat_response['items'][-1]
            author = last_message['authorDetails']['displayName']
            message = last_message['snippet']['displayMessage']
            print(f"{author}: {message}")

            # Call press_key if comment matches any key
            press_key(message)

        # Sleep for a few seconds before fetching new messages
        time.sleep(1)

# Replace with your live video ID
get_live_chat_messages('Mvr4NQF0IuQ')
