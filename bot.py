# %%
# import packages
%pip install spotipy
%pip install openai

# %%
import os
import getpass 
import openai
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from random import sample


# # Get OpenAI API key
# openai.api_key = getpass("Please enter your OpenAI API key: ")

# def define_spotify():
#     print("1: Enter your Spotify API key\n2: Enter your Spotify id or username")
#     spotify_option = input("Input (1 or 2): ")

#     if spotify_option not in ['1', '2']:
#         print("Must input either 1 or 2")
#         return define_spotify()

#     if spotify_option == '1':
#         return getpass("Please enter your Spotify API key: ")
    
#     elif spotify_option == '2':
#         print("1: Spotify ID\n2:  Enter your username")
#         spotify_optionUorC = input("Input (1 or 2): ")
        

#         if spotify_optionUorC not in ['1', '2']:
#             print("Must input either 1 or 2")
#             return define_spotify()
        
#         if spotify_optionUorC == '1':
#             username = input("Username: ")
#             scope = "user-library-read playlist-modify-public"


#         if spotify_optionUorC == '2':
#             clientID = input("ClientID: ")
#             scope = "user-library-read playlist-modify-public"
#             os.environ["SPOTIPY_CLIENT_SECRET"] = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=clientID ,open_browser=True,))



# spotify = define_spotify()


# Get OpenAI API key
openai.api_key = getpass.getpass("Please enter your OpenAI API key: ")

def define_spotify():
    print("1: Enter your Spotify API details\n2: Log in to your Spotify account")
    spotify_option = input("Input (1 or 2): ")

    if spotify_option not in ['1', '2']:
        print("Must input either 1 or 2")
        return define_spotify()

    if spotify_option == '1':
        client_id = getpass("Please enter your Spotify Client ID: ")
        client_secret = getpass("Please enter your Spotify Client Secret: ")
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    elif spotify_option == '2':
        print("Please log in to your Spotify account.")
        scope = "playlist-read-private playlist-read-collaborative user-library-read playlist-modify-public playlist-modify-private"
        auth_manager = SpotifyOAuth(scope=scope, open_browser=True)

    return spotipy.Spotify(auth_manager=auth_manager)

spotify = define_spotify()


# %%

def get_user_tracks():
    results = spotify.current_user_saved_tracks()
    return [track['track']['id'] for track in results['items']]

def get_related_tracks(user_tracks):
    related_tracks = []
    for track in user_tracks:
        related = spotify.artist_top_tracks(spotify.track(track)['artists'][0]['id'])
        related_tracks.extend([t['id'] for t in related['tracks']])
    return related_tracks

def gpt_prompt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60
    )
    return response.choices[0].text.strip()

def create_playlist(prompt):
    # Generate playlist name using GPT-4
    playlist_name = gpt_prompt(prompt)
    
    # Get user's tracks
    user_tracks = get_user_tracks()
    
    # Get related tracks
    related_tracks = get_related_tracks(user_tracks)
    
    # Get intersection of user's tracks and related tracks
    common_tracks = list(set(user_tracks) & set(related_tracks))
    
    # Create new playlist
    playlist = spotify.user_playlist_create(os.getenv("spotifyUSERNAME"), playlist_name)
    
    # Add half from user's tracks and half from related tracks
    half_length = len(common_tracks) // 2
    tracks_to_add = common_tracks[:half_length] + related_tracks[:half_length]
    
    # Add tracks to the playlist
    spotify.playlist_add_items(playlist['id'], tracks_to_add)

# Prompt for creating the playlist
prompt = "Create a playlist for coding and focusing."
create_playlist(prompt)


