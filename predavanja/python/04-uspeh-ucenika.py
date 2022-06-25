# https://petlja.org/biblioteka/r/Zbirka-python/uspeh_ucenika
prosek = float(input())

if prosek >= 4.5:
    uspeh = 'odlican'
elif prosek >= 3.5:
    uspeh = 'vrlodobar'
elif prosek >= 2.5:
    uspeh = 'dobar'
elif prosek >= 2:
    uspeh = 'dovoljan'
else:
    uspeh = 'nedovoljan'

# if prosek >= 4.5:
#     uspeh = 'odlican'
# if prosek < 4.5 or prosek >= 3.5:
#     uspeh = 'vrlodobar'

print(uspeh)
