tehtava = "Tee funktio joka ottaa inputtina lauseen (string), ja palauttaa list():in jossa lause jatkuu aina kymmenen kirjaimen jälkeen seuraavassa list-memberissä\
        Jos lause ei ole 10 kirjainta pitkä, palauttaa listin jossa koko lause ensimmäisessä memberissä"

lause  = "Lähdin samoilta hiekkalaatikoilta ja pihoilta joilta muutkin kotipojat vietiin nukkuun joka ilta"

#   rivitetty_lause = list()
#   list_lause = list()

#   def rivitetty(long_string, row_length):
#       rivitetty_long_string = list()
#       list_long_string = list()
#       for i in long_string:
#           list_long_string.append(i)

#       while len(list_long_string) > 0:
#           if len(list_long_string) > row_length:
#               rivitetty_long_string.append(list_long_string[0:row_length])
#               list_long_string[0:row_length] = []
#           elif len(list_long_string) <= row_length:
#               rivitetty_long_string.append(list_long_string)
#               list_long_string = []
#       print(rivitetty_long_string)

#       valmis_rivitetty = []
#       for i in rivitetty_long_string:
#           valmis_rivitetty.append("".join(i))
#       return valmis_rivitetty

def rivitetty(long_string, row_length):
    words = long_string.rsplit()
    rows = [[]]
    count = 0
    for i in words:
        if len(" ".join(rows[count]) + i)  < row_length:
            rows[count].append(i)
        else:
            rows.append([])
            count += 1
            rows[count].append(i)

    joined_rows = []
    for i in rows:
        joined_rows.append(" ".join(i))
    return joined_rows

for i in rivitetty(lause, 20):
    print(i)
