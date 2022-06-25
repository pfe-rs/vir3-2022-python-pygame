# https://petlja.org/biblioteka/r/Zbirka-python/izbacivanje_elemenata

n = int(input())

brojevi = []

for i in range(n):
    ucitani_broj = int(input())
    brojevi.append(ucitani_broj)

# print(brojevi)

while True:
    pozeljni_brojevi = []
    duzina = len(brojevi)
    for broj in brojevi:
        if duzina % broj == 0:
            continue
        pozeljni_brojevi.append(broj)
    # print(pozeljni_brojevi)
    if len(brojevi) == len(pozeljni_brojevi):
        break
    brojevi = pozeljni_brojevi

print(sum(brojevi))
