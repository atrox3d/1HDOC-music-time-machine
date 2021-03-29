import logging
import requests
from util import logger
import spotipy
import json
# from myob import spotify
import util.parentimport
if __name__ == "__main__":
    util.parentimport.add_import_absolute_folder("..")
else:
    util.parentimport.add_import_absolute_folder("../..")
from _myob.music_time_machine import myob

SPOTIFY_CLIENT_ID = myob.CLIENT_ID
SPOTIFY_CLIENT_SECRET = myob.CLIENT_SECRET
SPOTIFY_REDIRECT_URY = "http://localhost:1970"
SPOTIFY_CLIENT_SCOPE = "playlist-modify-private"


class SpotifyConnector:
    """
    proxy to spotpy module
    """
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
            enable_library_logging=False,
    ):
        """
        save references to spotipy parameters
        :param debug:
        :param client_id:
        :param client_secret:
        :param redirect_uri:
        :param scope:
        :param show_dialogue:
        :param cache_path:
        """
        self.debug = debug
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.show_dialogue = show_dialogue
        self.cache_path = cache_path
        self.oauth: spotipy.SpotifyOAuth = None
        self.client: spotipy.Spotify = None
        self.logger = logger.get_cli_logger("CLASS:" + __class__.__name__)
        self.logger.setLevel("DEBUG")
        self.spotipyLogger = spotipy.client.logger
        if enable_library_logging:
            self.spotipyLogger.addHandler(logging.StreamHandler())
            self.spotipyLogger.setLevel(logging.DEBUG)
            self.spotipyLogger.info("WOOOOOOOOOOOOOOOOOOOOOOO")



    @logger.logger_decorator_with_arguments(True)
    def get_oauth(self) -> spotipy.oauth2.SpotifyOAuth:
        """
        creates a spotipy.oauth2.SpotifyOAuth object
        :return:
        """
        # _logger = self.get_oauth.logger
        self.logger.debug(f"self.oauth = spotipy.oauth2.SpotifyOAuth(")
        self.logger.debug(f"    client_id={self.client_id},")
        self.logger.debug(f"    client_secret={self.client_secret},")
        self.logger.debug(f"    redirect_uri={self.redirect_uri},")
        self.logger.debug(f"    scope={self.scope},")
        self.logger.debug(f"    show_dialog={self.show_dialogue},")
        self.logger.debug(f"    cache_path={self.cache_path}")
        self.logger.debug(f")")
        if self.debug:
            self.logger.debug("debug is active, not calling API")
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
        """
        creates a spotipy.Spotify client object
        :return:
        """
        self.logger.debug(f"auth = self.get_oauth()")
        auth = self.get_oauth()
        self.logger.debug(f"self.client = spotipy.Spotify(auth_manager=auth)")
        if self.debug:
            return None
        else:
            self.client = spotipy.Spotify(auth_manager=auth)
            return self.client

    @logger.logger_decorator_with_arguments(True)
    def search_track(self, song, year, artist):
        # q_uri = f"track:{song} year:{year}"
        # q_uri = f'artist:"{artist}" "{song}" year:{year}'
        song = song.lower()
        song = song.replace("'", " ")
        artist = artist.lower()
        artist = artist.replace("featuring", "")
        q_uri = f'{song} artist:{artist}'
        self.logger.debug(f"QUERY : q={q_uri}")
        print(f"q={q_uri}")
        result = self.client.search(q=q_uri, type="track")

        print("-" * 80)
        for song_item in result["tracks"]["items"]:
            song_name = song_item["name"]
            for artist_item in song_item["artists"]:
                artist_name = artist_item["name"]
                print(f"SONG: {song_name}, ARTIST: {artist_name}")
        print("-" * 80)

        try:
            song_uri = result["tracks"]["items"][0]["uri"]
            self.logger.info(f"OK    | {song_uri}")
            return song_uri
        except IndexError:
            self.logger.error(f"ERROR | {song} NOT found")
            return None

    @logger.logger_decorator_with_arguments(True)
    def dump_spotify_token(self):
        with open(self.cache_path) as cachefile:
            j = json.load(cachefile)
            print(json.dumps(j, indent=4))


if __name__ == "__main__":
    spc = SpotifyConnector()
