from billboard import Billboard
from spotify import SpotifyConnector
import json

import util

date = "1981-12-27"     # adriano
date = "1938-03-29"     # papà
date = "1978-05-23"     # silvia
date = "1970-07-13"     # io
date = "1982-07-21"     # cika
if not date:
    # TODO: add regex for input validation
    date = input("when do you want to go? insert date in this format YYYY-MM-DD: ")

bb = Billboard()

h100 = bb.get_songlist(date, test="test", test2=2)
h100.list()
# exit()

spc = SpotifyConnector(debug=False)
sp = spc.get_client()
print(type(sp.me()))
print(
    json.dumps(sp.me(), indent=4)
)

print(spc.get_token())

year = date.split("-")[0]
song_uris = []
found = 0
not_found = 0
# for song in h100.songs:
for index in range(len(h100.songs)):
    song = h100.songs[index]
    artist = h100.artists[index]
    print(f"SONG  : {song}")
    print(f"ARTIST: {artist}")
    print(f"YEAR  : {year}")
    # q_uri = f"track:{song} year:{year} artist:{artist}"
    q_uri = f"track:{song} year:{year}"
    print(f"QUERY : q={q_uri}")
    result = sp.search(q=q_uri, type="track")
    # print(json.dumps(result, indent=4))
    try:
        song_uri = result["tracks"]["items"][0]["uri"]
        print(f"OK    | {song_uri}")
        song_uris.append(song_uri)
        found += 1
    except IndexError:
        print(f"ERROR | {q_uri} NOT found")
        song_uris.append("NOT FOUND")
        not_found += 1
    pass

print(f"found songs: {found}, not found songs: {not_found}")