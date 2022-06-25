# Motivacija:
# podatak1 = 1
# podatak2 = 2
# ...

podatak = [1, 2, ...]

# Pravljenje liste:
lista_brojeva = [1, 2, 3, 4, 5, 4]
lista_stringova = ['abc', 'def', 'ghj']
lista_svacega = [1, 2, 'abc', 5.5, True, [1, 2, 3]]
prazna_lista = []
lista_sa_none = [None]

# Dodavanje u listu:
prazna_lista.append(1)
# print(prazna_lista)

# Pristupanje elementima liste:
# print(prazna_lista[0])
# print(lista_brojeva[-1])
# print(lista_brojeva[-2])
# print(prazna_lista[10]) #-> greška
# print(prazna_lista[-15]) #-> greška

# Menjanje elementa liste:
prazna_lista[0] = 2
# print(prazna_lista)

# Provera dužine liste:
# print(len(lista_brojeva))

# Provera pripadnosti listi:
# print(1 in prazna_lista)
# print(1 not in prazna_lista)
# print(2 in prazna_lista)
# print(prazna_lista.index(2))

# Uklanjanje iz liste:
del lista_brojeva[2]
lista_brojeva.remove(4)
# lista_brojeva.pop()
# print(lista_brojeva)

# Spajanje dve liste:
prazna_lista += [2]
lista_svega_i_svacega = lista_svacega + [1, 2, 3]
# print(lista_svega_i_svacega)
# print(prazna_lista)

# Pristup opsegu liste:
# print(lista_brojeva)
# print(lista_brojeva[1:3])
# print(lista_brojeva[1:])
# print(lista_brojeva[:3])
# print(lista_brojeva[::2])
# print(lista_brojeva[::-1])

# Korisne funkcije za rad sa listima:
# print(min(lista_brojeva))
# print(max(lista_brojeva))
# print(sum(lista_brojeva))
# avg()

# Dokumentacija:
# - https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
# - https://docs.python.org/3/library/functions.html

# Problem sa kopiranjem liste:
# [1, 2, 5, 4] (lista_brojeva, nova_lista_brojeva)
nova_lista_brojeva = lista_brojeva
nova_lista_brojeva += [1]
print(nova_lista_brojeva)
print(lista_brojeva)
# Rešenje problema:
zapravo_nova_lista_brojeva = lista_brojeva[:]
zapravo_nova_lista_brojeva.append(1)
print(lista_brojeva)

# 1 (a)
# 1 (b)
a = 1
b = a
b = 2
print(a, b)
