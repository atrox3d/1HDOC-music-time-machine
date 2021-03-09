from util import logger


class Hot100:
    @logger.logger_arguments(True)
    def __init__(self, date: str, positions: list, songs: list, artists: list):
        self.date = date
        self.positions = positions.copy()
        self.songs = songs.copy()
        self.artists = artists.copy()

    @logger.logger_arguments(True)
    def list(self):
        for i in range(len(self.positions)):
            print(f"{self.positions[i]:3d} - {self.songs[i]} - {self.artists[i]}")

