


import os
import spotipy
import openai
from spotipy.oauth2 import SpotifyOAuth
from random import sample

# Setup OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup Spotify API
scope = "user-library-read playlist-modify-public"
username = os.getenv("SPOTIFY_USERNAME")
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))

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

def create_playlist(prompt, username):
    # Generate playlist name using GPT-4
    playlist_name = gpt_prompt(prompt)
    
    # Get user's tracks
    user_tracks = get_user_tracks()
    
    # Get related tracks
    related_tracks = get_related_tracks(user_tracks)
    
    # Get intersection of user's tracks and related tracks
    common_tracks = list(set(user_tracks) & set(related_tracks))
    
    # Create new playlist
    playlist = spotify.user_playlist_create(username, playlist_name)
    
    # Add half from user's tracks and half from related tracks
    half_length = len(common_tracks) // 2
    tracks_to_add = common_tracks[:half_length] + related_tracks[:half_length]
    
    # Add tracks to the playlist
    spotify.playlist_add_items(playlist['id'], tracks_to_add)

# Prompt for creating the playlist
prompt = "Create a playlist for coding and focusing."
create_playlist(prompt, username)
