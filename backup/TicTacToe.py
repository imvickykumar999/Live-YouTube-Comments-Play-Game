import os
import time
from googleapiclient.discovery import build

def initialize_board():
    return {
        1: ' 1', 2: ' 2', 3: ' 3',
        4: ' 4', 5: ' 5', 6: ' 6',
        7: ' 7', 8: ' 8', 9: ' 9'
    }

def printBoard(board):
    n = 16
    print()
    print('-' * n)
    print('| ' + board[1] + ' | ' + board[2] + ' | ' + board[3] + ' |')
    print('-' * n)
    print('| ' + board[4] + ' | ' + board[5] + ' | ' + board[6] + ' |')
    print('-' * n)
    print('| ' + board[7] + ' | ' + board[8] + ' | ' + board[9] + ' |')
    print('-' * n)
    print()

def checkBoard(board):
    # Check for winner
    winning_combinations = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Horizontal
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Vertical
        (1, 5, 9), (3, 5, 7)              # Diagonal
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]]:
            print(board[combo[0]] + " Won!")
            return True
    return False

def get_live_chat_messages(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Get live chat ID
    video_response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()

    if 'items' not in video_response or not video_response['items']:
        print("No live video found with the provided ID.")
        return None

    live_chat_id = video_response['items'][0].get('liveStreamingDetails', {}).get('activeLiveChatId')
    if not live_chat_id:
        print("Live chat not available for this video.")
        return None

    print("Fetching live chat messages...")
    return youtube, live_chat_id

def play_tic_tac_toe(youtube, live_chat_id):
    board = initialize_board()
    ox = 1  # Player 1 starts
    mykey = []
    value = ['😄', '❌']

    printBoard(board)
    print("Live chat comments will now control the game!")
    print("Enter numbers (1-9) in the live chat to make moves.")

    while True:
        # Fetch live chat messages
        chat_response = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part='snippet,authorDetails'
        ).execute()

        # Get the last message from chat
        if 'items' in chat_response and chat_response['items']:
            last_message = chat_response['items'][-1]['snippet']['displayMessage']

        try:
            # Attempt to interpret the message as a move
            key = int(last_message.strip())
            if key in range(1, 10) and key not in mykey:
                mykey.append(key)
                board[key] = value[ox % 2]
                ox += 1

                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
                printBoard(board)

                # Check for a winner
                if checkBoard(board):
                    print()
                    print('Game will restart with in 10 sec.')
                    time.sleep(10)  # Wait for 10 seconds before restarting
                    return  # Exit the current game loop to restart

                # Check for a draw
                if len(mykey) == 9:
                    print()
                    print('Game will restart with in 10 sec.')
                    time.sleep(10)  # Wait for 10 seconds before restarting
                    return  # Exit the current game loop to restart
            else:
                # Clear screen and reprint the board along with the message
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
                printBoard(board)
                print(f"{value[ox % 2]}'s turn.")
        except ValueError:
            # Ignore non-integer comments
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
            printBoard(board)
            print(f"{value[ox % 2]}'s turn.")

        # Poll every second
        time.sleep(1)

def tic_tac_toe_with_live_chat(video_id, api_key):
    youtube, live_chat_id = get_live_chat_messages(video_id, api_key)
    if not youtube or not live_chat_id:
        return

    while True:
        # time.sleep(3)
        play_tic_tac_toe(youtube, live_chat_id)  # Restart the game after it ends

# Replace these values with your YouTube video ID and API key
VIDEO_ID = 'lqtkoPsNTWM'  # Replace with your live video ID

# https://console.cloud.google.com/apis/credentials/key/83da1257-e24d-484f-924b-d7879612b6ff?project=imvickykumar999-1723015985916
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Replace with your API key
tic_tac_toe_with_live_chat(VIDEO_ID, API_KEY)
