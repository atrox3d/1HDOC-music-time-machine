from billboard.billboard import Billboard
from spotify.spotify import SpotifyConnector

date = "1981-12-27"     # adriano
date = "1938-03-29"     # papà
date = "1982-07-21"     # cika
date = "1970-07-13"     # io
date = "1978-05-23"     # silvia
if not date:
    # TODO: add regex for input validation
    date = input("when do you want to go? insert date in this format YYYY-MM-DD: ")

bb = Billboard()
h100 = bb.get_songlist(date)

h100.list()

spc = SpotifyConnector(debug=False)
sp = spc.get_client()

print(sp.me())

