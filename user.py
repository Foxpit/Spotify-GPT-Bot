import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import traceback

class User:
    
    
    def __init__(self, term="long_term"):
        scope = 'user-read-recently-played user-top-read user-library-read playlist-read-private playlist-read-collaborative'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                                            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                                                            scope=scope))
        self.term = term
        self.top_genres = None
        self.top_genres_artists = None

    def select_genre(self, idx=0):
        try:
            return list(self.top_genres.keys())[idx]
        except IndexError:
            raise IndexError("Index is out of range. Please provide a valid index.")

    def _get_tracks_from_results(self, results, key):
        try:
            return [track[key]['id'] for track in results['items']]
        except Exception as e:
            traceback.print_exc()
            print(f"Error getting {key}: {e}")
            return []

    def get_recently_played_tracks(self, limit=10):
        try:
            results = self.sp.current_user_recently_played(limit=limit)
            return self._get_tracks_from_results(results, 'track')
        except Exception as e:
            traceback.print_exc()
            raise Exception("Error getting recently played tracks:", e)

    def get_saved_tracks(self, limit=10):
        try:
            results = self.sp.current_user_saved_tracks(limit=limit)
            return self._get_tracks_from_results(results, 'track')
        except Exception as e:
            traceback.print_exc()
            print("Error getting saved tracks:", e)
            return []

    def get_saved_albums(self, limit=10):
        try:
            results = self.sp.current_user_saved_albums(limit=limit)
            return [album['album']['id'] for album in results['items']]
        except Exception as e:
            traceback.print_exc()
            print("Error getting saved albums:", e)
            return []

    def get_top_artists(self, limit=10):
        try:
            results = self.sp.current_user_top_artists(time_range=self.term, limit=limit)
            return [artist['id'] for artist in results['items']]
        except Exception as e:
            traceback.print_exc()
            print("Error getting top artists:", e)
            return []

    def get_top_tracks(self, limit=10):
        try:
            results = self.sp.current_user_top_tracks(limit=limit)
            return [track['id'] for track in results['items']]
        except Exception as e:
            traceback.print_exc()
            print("Error getting top tracks:", e)
            return []

    def get_top_genres(self):
        try:
            results = self.sp.current_user_top_artists(time_range=self.term, limit=100)
            all_genres = [genre for r in results['items'] for genre in r['genres']]
            top_genres = Counter(all_genres)
            self.top_genres = {key: value for key, value in sorted(top_genres.items(), key=lambda k: k[1], reverse=True)}
            self.top_genres_artists = [[r['name'], r['id'], r['genres']] if len(r['genres']) > 0 else [r['name'], r['id'], ['unknown genre']] for r in results['items']]
        except Exception as e:
            traceback.print_exc()
            print("Error getting top genres:", e)

    def get_genre_artists(self, genre):
        try:
            artists = []
            for name, _, genres in self.top_genres_artists:
                if genre in genres:
                    artists.append(name)
            artists = ", ".join(artists)
            return artists
        except Exception as e:
            traceback.print_exc()
            print("Error getting artists in genre:", e)
            return ""

    def get_user_playlists_by_name(self, playlist_name):
        try:
            playlists, offset = [], 0
            while True:
                response = self.sp.search(q=playlist_name, type="playlist", limit=50, offset=offset)
                playlists += [{"name": playlist["name"], "id": playlist["id"]} for playlist in response["playlists"]["items"]]
                if response["playlists"]["next"] is None:
                    break
                offset += 50
            return playlists
        except Exception as e:
            traceback.print_exc()
            print("Error getting user playlists by name:", e)
            return []

    def get_user_playlists_by_id(self, playlist_id):
        try:
            playlist = self.sp.playlist(playlist_id)
            return playlist
        except Exception as e:
            traceback.print_exc()
            print("Error getting user playlist by ID:", e)
            return {}

    def execute_playlist_code(self, playlist_id, code, comments=""):
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-read-private,playlist-read-collaborative"))
        except Exception as e:
            traceback.print_exc()
            error_message = "There was an error connecting to your Spotify account: {}\n\n{}".format(e, traceback.format_exc())
            return error_message, traceback.format_exc()

        playlist = sp.playlist(playlist_id)
        namespace = {"playlist_id": playlist_id, "playlist": playlist, "sp": sp, "answer": "Your question was unable to be answered."}

        try:
            exec(code, namespace)
        except Exception as e:
            traceback.print_exc()
            error_message = "There was an error executing the code generated by GPT: {}\n\n{}".format(e, traceback.format_exc())
            return error_message, traceback.format_exc()

        answer = f"{namespace['answer']}<br><br><strong>Comments:</strong><br>{comments}" if comments else namespace['answer']

        return answer, None
