import spotipy
from spotipy.oauth2 import SpotifyOAuth

YOUR_UNIQUE_CLIENT_ID = ""
YOUR_UNIQUE_CLIENT_SECRET = ""

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=YOUR_UNIQUE_CLIENT_ID,
        client_secret=YOUR_UNIQUE_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
