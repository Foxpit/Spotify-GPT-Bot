import os
import getpass
import openai
from user import User
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Get OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if (openai.api_key is None):
    print("Environment variable not set. Requesting user input...")
    openai.api_key = getpass.getpass("Please enter your OpenAI API key: ")


def handle_bot(data):
    # Create user instance
    user = User()

    # Get user's top genres
    user.get_top_genres()

    # Select a top genre
    top_genre = user.select_genre()

    # Get artists of the selected genre
    artists = user.get_genre_artists(top_genre)

    # Generate playlist name
    playlist_name = f"{top_genre} playlist by {artists}"

    # Create new playlist
    playlist = user.sp.user_playlist_create(
            os.getenv("SPOTIFY_USERNAME"),
            playlist_name
        )

    return {
            'status': 'Playlist created successfully',
            'playlist_name': playlist_name
        }


# def handle_bot(data):
#     def define_spotify():
#         client_id = os.getenv("SPOTIFY_CLIENT_ID")
#         client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
#         auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#         return spotipy.Spotify(auth_manager=auth_manager)

#     spotify = define_spotify()

#     def get_user_tracks():
#         results = spotify.current_user_saved_tracks()
#         return [track['track']['id'] for track in results['items']]

#     def get_related_tracks(user_tracks):
#         related_tracks = []
#         for track in user_tracks:
#             related = spotify.artist_top_tracks(spotify.track(track)['artists'][0]['id'])
#             related_tracks.extend([t['id'] for t in related['tracks']])
#         return related_tracks

#     def gpt_prompt(prompt):
#         response = openai.Completion.create(
#             engine="text-davinci-002",
#             prompt=prompt,
#             max_tokens=60
#         )
#         return response.choices[0].text.strip()

#     # Generate playlist name using GPT-4
#     playlist_name = gpt_prompt(data['prompt'])

#     # Get user's tracks
#     user_tracks = get_user_tracks()

#     # Get related tracks
#     related_tracks = get_related_tracks(user_tracks)

#     # Get intersection of user's tracks and related tracks
#     common_tracks = list(set(user_tracks) & set(related_tracks))

#     # Create new playlist
#     playlist = spotify.user_playlist_create(os.getenv("SPOTIFY_USERNAME"), playlist_name)

#     # Add half from user's tracks and half from related tracks
#     half_length = len(common_tracks) // 2
#     tracks_to_add = common_tracks[:half_length] + related_tracks[:half_length]

#     # Add tracks to the playlist
#     spotify.playlist_add_items(playlist['id'], tracks_to_add)

#     return {'status': 'Playlist created successfully'}
