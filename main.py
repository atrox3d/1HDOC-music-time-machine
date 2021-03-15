from billboard import Billboard
from spotify import SpotifyConnector
import json
import util.logger

date = "1981-12-27"     # adriano
date = "1938-03-29"     # papà
date = "1978-05-23"     # silvia
date = "1970-07-13"     # io
date = "1982-07-21"     # cika
if not date:
    # TODO: add regex for input validation
    date = input("when do you want to go? insert date in this format YYYY-MM-DD: ")

util.logger.disable()

bb = Billboard()

h100 = bb.get_songlist(date, testlogger1="test", testlogger2=2)
h100.list()

spconn = SpotifyConnector(debug=False)
spcli = spconn.get_client()
print("me(): ", type(spcli.me()))
print(
    json.dumps(spcli.me(), indent=4)
)

print("token")
spconn.dump_spotify_token()

year = date.split("-")[0]
song_uris = []
found = 0
not_found = 0
for index in range(len(h100.songs)):
    song = h100.songs[index]
    artist = h100.artists[index]
    print(f"SONG  : {song}")
    print(f"ARTIST: {artist}")
    print(f"YEAR  : {year}")
    song_uri = spconn.search_track(song, year)
    if song_uri:
        print(f"OK    | {song_uri}")
        song_uris.append(song_uri)
        found += 1
    else:
        print(f"ERROR | {song} NOT found")
        song_uris.append("NOT FOUND")
        not_found += 1
    pass

print(f"found songs: {found}, not found songs: {not_found}")


