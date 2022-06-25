# https://petlja.org/biblioteka/r/Zbirka-python/cezarov_kod

tekst = input()
pomak = int(input())
smer = int(input())

if smer == 2:
    pomak = -pomak

sifrovan_tekst = ''

for karakter in tekst:
    # karakter -> [97, 122] -> [0, 25] -> šifrovanje -> [0, 25] -> [97, 122] -> karakter
    sifrovani_karakter = chr((ord(karakter) - ord('a') + pomak) % 26 + ord('a'))
    sifrovan_tekst += sifrovani_karakter

print(sifrovan_tekst)
