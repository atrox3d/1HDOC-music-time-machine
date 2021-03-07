from billboard.billboard import Billboard

# date = "1981-12-27"
# date = "1938-03-29"
# date = "1982-07-21"
date = "1970-07-13"
if not date:
    # TODO: add regex for input validation
    date = input("when do you want to go? insert date in this format YYYY-MM-DD: ")

bb = Billboard()
h100 = bb.get_songlist(date)

h100.list()

