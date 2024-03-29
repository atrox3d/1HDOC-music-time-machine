from .cache import BillboardCache
from .hot100_model import Hot100
import requests
import bs4
from bs4 import BeautifulSoup
from util import logger
# import logging

BASE_URL = "https://www.billboard.com/charts/hot-100"


class Billboard:
    # log = logger.get_cli_logger(__qualname__)

    @logger.logger_decorator_with_arguments(True)
    def __init__(self):
        self.cache = BillboardCache()
        self.date = ""
        self.url = BASE_URL
        self.current_url = ""
        self.positions = []
        self.songs = []
        self.artists = []
        # Billboard.log.info("")

    @logger.logger_decorator_with_arguments(True)
    def get_page(self, date):
        # Billboard.log.info("")
        self.current_url = f"{self.url}/{date}"
        if self.cache.is_cached(date):
            print(f"date {date} found in cache, loading local copy...")
            page = self.cache.load(date)
        else:
            print(f"date {date} not found in cache, downloading...")
            response = requests.get(self.current_url)
            response.raise_for_status()
            page = response.text

            print(f"saving local copy of {self.current_url}...")
            self.cache.save(date, page)

        return page

    @logger.logger_decorator_with_arguments(True)
    def get_songlist(self, date: str, **kwargs) -> Hot100:
        # Billboard.log.info("")
        self.date = date
        page = self.get_page(self.date)
        print(f"scanning: {self.current_url}...")
        soup = BeautifulSoup(page, "html.parser")

        rank_class = "chart-element__rank__number"
        song_class = "chart-element__information__song"
        artist_class = "chart-element__information__artist"

        self.positions = [int(position.getText()) for position in soup.find_all(name="span", class_=rank_class)]
        self.songs = [song.getText() for song in soup.find_all(name="span", class_=song_class)]
        self.artists = [artist.getText() for artist in soup.find_all(name="span", class_=artist_class)]

        hot100 = Hot100(
            date=self.date,
            url=self.current_url,
            positions=self.positions,
            songs=self.songs,
            artists=self.artists
        )
        return hot100
