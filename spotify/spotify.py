from util import logger
import spotipy
from myob import spotify
import json

SPOTIFY_CLIENT_ID = spotify.CLIENT_ID
SPOTIFY_CLIENT_SECRET = spotify.CLIENT_SECRET
SPOTIFY_REDIRECT_URY = "http://localhost:1970"
SPOTIFY_CLIENT_SCOPE = "playlist-modify-private"


class SpotifyConnector:
    @logger.logger_decorator_with_arguments(True)
    def __init__(
            self,
            debug=True,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URY,
            scope=SPOTIFY_CLIENT_SCOPE,
            show_dialogue=True,
            cache_path="myob/token.txt",
    ):
        self.debug = debug
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.show_dialogue = show_dialogue
        self.cache_path = cache_path
        self.oauth = None
        self.client = None

    @logger.logger_decorator_with_arguments(True)
    def get_oauth(self) -> spotipy.oauth2.SpotifyOAuth:
        print(f"self.oauth = spotipy.oauth2.SpotifyOAuth(")
        print(f"    client_id={self.client_id},")
        print(f"    client_secret={self.client_secret},")
        print(f"    redirect_uri={self.redirect_uri},")
        print(f"    scope={self.scope},")
        print(f"    show_dialog={self.show_dialogue},")
        print(f"    cache_path={self.cache_path}")
        print(f")")
        if self.debug:
            return None
        else:
            self.oauth = spotipy.oauth2.SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
                show_dialog=self.show_dialogue,
                cache_path=self.cache_path
            )
            return self.oauth

    @logger.logger_decorator_with_arguments(True)
    def get_client(self) -> spotipy.Spotify:
        print(f"auth = self.get_oauth()")
        auth = self.get_oauth()
        if self.debug:
            print(f"self.client = spotipy.Spotify(auth_manager=auth)")
            return None
        else:
            self.client = spotipy.Spotify(auth_manager=auth)
            return self.client

    @logger.logger_decorator_with_arguments(True)
    def get_token(self):
        with open(self.cache_path) as cachefile:
            j = json.load(cachefile)
            print(json.dumps(j, indent=4))
