import requests
import bs4
from bs4 import BeautifulSoup

BASE_URL = "https://www.billboard.com/charts/hot-100"
CACHE_DIR = "billboard-cache"


def load_page(date):
    with open(f"{CACHE_DIR}/{date}.html", mode="r", encoding="utf-8") as cachefile:
        page = cachefile.read()
        return page


def save_page(date, page):
    with open(f"{CACHE_DIR}/{date}.html", mode="w", encoding="utf-8") as cachefile:
        cachefile.write(page)


def is_cached(date):
    try:
        with open(f"{CACHE_DIR}/{date}.html", mode="r", encoding="utf-8") as cachefile:
            return True
    except FileNotFoundError:
        return False


########################################################################################################################
#
#   MAIN
#
########################################################################################################################
# date = "1981-12-27"
# date = "1938-03-29"
date = "1970-07-13"
if not date:
    # TODO: add regex for input validation
    date = input("when do you want to go? insert date in this format YYYY-MM-DD: ")
url = f"{BASE_URL}/{date}"

position = ""
if is_cached(date):
    print(f"date {date} found in cache, loading local copy...")
    page = load_page(date)
else:
    print(f"date {date} not found in cache, downloading...")
    response = requests.get(url)
    response.raise_for_status()
    page = response.text

    print(f"saving local copy of {url}...")
    save_page(date, page)

print(f"scanning: {url}...")
soup = BeautifulSoup(page, "html.parser")

positions = [int(position.getText()) for position in soup.find_all(name="span", class_="chart-element__rank__number")]
songs = [song.getText() for song in soup.find_all(name="span", class_="chart-element__information__song")]
artists = [artist.getText() for artist in soup.find_all(name="span", class_="chart-element__information__artist")]

for i in range(len(positions)):
    print(f"{positions[i]:3d} - {songs[i]} - {artists[i]}")
