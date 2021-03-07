CACHE_DIR = "billboard-cache"


class BillboardCache:
    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache = []

    def load(self, date):
        with open(f"{self.cache_dir}/{date}.html", mode="r", encoding="utf-8") as cachefile:
            page = cachefile.read()
            return page

    def save(self, date, page):
        with open(f"{self.cache_dir}/{date}.html", mode="w", encoding="utf-8") as cachefile:
            cachefile.write(page)

    def is_cached(self, date):
        if date in self.cache:
            try:
                with open(f"{self.cache_dir}/{date}.html", mode="r", encoding="utf-8") as _:
                    return True
            except FileNotFoundError:
                return False
        else:
            return False
