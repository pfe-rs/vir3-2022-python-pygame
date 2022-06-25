# Pravljenje stringa
neki_tekst = 'neki tekst'
# neki_tekst = "neki tekst"

# Isto kao kod lista:
# - pristup karakteru i opsegu
# print(neki_tekst[0])
# print(neki_tekst[5:])
# print(neki_tekst[::-1])

# - dužina stringa
# print(len(neki_tekst))

# - provera pripadnosti stringu
# print('tekst' in neki_tekst)

# - nadovezivanje
# print(neki_tekst + ' tekst')

# Poređenje stringova
# print('abc' < 'zbc')
# print('abc' < 'abz')
# print('abc' < 'abcd')

# Specijalne sekvence
# string_sa_novom_linijom = 'prva linija\ndruga linija'
# print(string_sa_novom_linijom)
# drugi_string_sa_novom_linijom = '''prva linija
# druga linija'''
# print(drugi_string_sa_novom_linijom)
# string_sa_tabovima = 'a\tb\tc\td'
# print(string_sa_tabovima)

# Podela stringa
# linija = input().split()
# 1 2
# print(linija)
# prvi_broj = int(linija[0])
# drugi_broj = int(linija[1])
# print(prvi_broj + drugi_broj)


# Korisne funkcije za rad sa stringovima
print(neki_tekst.upper())
print(neki_tekst.startswith('neki'))
print(neki_tekst.replace('neki', 'ovaj'))

# Dokumentacija: https://docs.python.org/3/library/stdtypes.html#textseq
