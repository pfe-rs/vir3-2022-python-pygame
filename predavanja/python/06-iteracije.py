# while
a = 0
while a < 3:
    a += 1
    # print(a)

# for po listi
# C kod:
# for (int i = 0; i < N; ++i) {
#     cout << lista[i];
# }
# for (int element : lista) {
#     cout << element;
# }
# <=>
# Python kod:
lista = [1, 2, 3]
# for element in lista:
#     print(element)

# for sa brojačem
# C kod:
# for (int i = 0; i < 5; ++i) {
#     cout << i;
# }
# <=>
# Python kod:
# range(5) <=> [0, 1, 2, 3, 4]
# for i in range(5):
#     print(i)

# for po listi sa brojačem
# C kod
# <=>
# for (int i = 0; i < N; ++i) {
#     cout << i << " " << lista[i];
# }
# Python kod:
lista_stringova = ['a', 'b', 'c']
# enumerate(lista_stringova) <=> [[0, 'a'], [1, 'b'], [2, 'c']]
# for i, element in enumerate(lista_stringova):
#     print(i, element)

# break, continue, pass:
b = 0
while True:
    b += 1
    if b % 2 == 0:
        continue
    print(b)
    if b % 5 == 0:
        break
