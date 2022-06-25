# https://petlja.org/biblioteka/r/Zbirka-python/broj_bombi_u_okolini

# matrica = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]

linija = input().split()
m = int(linija[0])
n = int(linija[1])

matrica = []

for vrsta in range(m):
    ucitani_red = input().split()
    red = []
    for element in ucitani_red:
        red.append(int(element))
    matrica.append(red)

broj_bombi = []

for vrsta in range(m):
    red = []
    for kolona in range(n):
        broj = 0
        if vrsta != 0:
            # Gore
            broj += matrica[vrsta-1][kolona]
        if vrsta != m-1:
            # Dole
            broj += matrica[vrsta+1][kolona]
        if kolona != 0:
            # Levo
            broj += matrica[vrsta][kolona-1]
        if kolona != n-1:
            # Desno
            broj += matrica[vrsta][kolona+1]
        if vrsta != 0 and kolona != 0:
            # Gore levo
            broj += matrica[vrsta-1][kolona-1]
        if vrsta != m-1 and kolona != 0:
            # Dole levo
            broj += matrica[vrsta+1][kolona-1]
        if vrsta != 0 and kolona != n-1:
            # Gore desno
            broj += matrica[vrsta-1][kolona+1]
        if vrsta != m-1 and kolona != n-1:
            # Dole desno
            broj += matrica[vrsta+1][kolona+1]
        red.append(broj)
    broj_bombi.append(red)

for red in broj_bombi:
    for broj in red:
        print(broj, end=' ')
    print()
