from googleapiclient.discovery import build
import time

def get_live_chat_messages(video_id):
    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey='AIzaSyCcJX4qdbo9caqxZSKDmuBjNVWfvq8_Wcs')

    # Get live chat ID
    video_response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()

    live_chat_id = video_response['items'][0]['liveStreamingDetails'].get('activeLiveChatId')

    if not live_chat_id:
        print("Live chat not available for this video.")
        return

    # Fetch live chat messages in a loop
    while True:
        chat_response = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part='snippet,authorDetails'
        ).execute()

        # Print each message
        for item in chat_response['items']:
            author = item['authorDetails']['displayName']
            message = item['snippet']['displayMessage']
            print(f"{author}: {message}")

        # Sleep for a few seconds before fetching new messages
        time.sleep(5)

# Replace with your live video ID
get_live_chat_messages('Mvr4NQF0IuQ')
