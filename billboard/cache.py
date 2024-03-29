from util import logger
CACHE_DIR = "billboard-cache"


class BillboardCache:
    @logger.logger_decorator_with_arguments(True)
    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = cache_dir
        # self.cache = []

    @logger.logger_decorator_with_arguments(True)
    def load(self, date):
        with open(f"{self.cache_dir}/{date}.html", mode="r", encoding="utf-8") as cachefile:
            page = cachefile.read()
            return page

    @logger.logger_decorator_with_arguments(True)
    def save(self, date, page):
        with open(f"{self.cache_dir}/{date}.html", mode="w", encoding="utf-8") as cachefile:
            cachefile.write(page)

    @logger.logger_decorator_with_arguments(True)
    def is_cached(self, date):
        # if date in self.cache:
        try:
            with open(f"{self.cache_dir}/{date}.html", mode="r", encoding="utf-8") as _:
                # self.cache.append(date)
                return True
        except FileNotFoundError:
            return False
        # else:
        #     return False
