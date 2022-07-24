# Asteroids (Asteroidi)

Autor: Vuk Mićović

Projekat je kao zadatak imao cilj rekreacije igrice "Asteroids" iz 1979. koristeći Python + `pygame` biblioteku.

## Napomene
- Sličice asteroida i broda su ručno napravljene
- Projekat koristi `math` biblioteku umesto optimizovanije `numpy` biblioteke za proračune
- Rad **nije** objašnjen komentarima
- Podešavanja (promenljive) **nisu** dokumentovana
- Sve definicije klasa, funkcija i promenljivih su zgusnute u 2 (dva) fajla
- Refresh rate/FPS je zakljucan na 60
- Brzina kretanja broda pod određenim uglovima nije dobro raspoređena po osama (X i Y)
- Iz originalne igrice nedostaju: Leteći brodovi kao neprijatelji (mali i veliki), njihovi zvuci i sličice

## Potrebne biblioteke
- Testirano koristeći `Python 3.10.5`
- `pygame` (testirano verzijom 2.1.2)

## Pokretanje
Instalirati `pygame` biblioteku:
```bash
pip3 install pygame
```
Pokrenuti igricu:
```bash
python3 main.py
```

## Testiranje
Videti [Pokretanje](<#pokretanje>)

Testovi su prošli uspešno ako sve komponente igre (zvuk, pomeranje, detekcija pogodaka, prikaz poena, sistem života...) prividno rade, bez grešaka u konzoli.
