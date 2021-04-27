import generator as gen
import numpy as np

moduleName = '../CPLEX/generator'

n = 3
Z = 4124
generator = gen.RandomNumberGenerator(Z)

X = []
PoczatkoweWybrane = np.zeros(n, dtype=bool)

C = np.zeros(n)
W = np.zeros(n)
B = generator.nextInt(5*n, 10*n)
for i in range(0, n):
    C[i] = generator.nextInt(1, 30)
    W[i] = generator.nextInt(1, 30)
    PoczatkoweWybrane[i] = False

# BRUTE FORCE


def szukajRozwiazania(X, PWybrane, wybor, poziom, biezacyNajlepszy):

    PWybrane[wybor] = True
    X.append(wybor)
    sumaWag = sumujWagi(X)
    print("Poziom: ", poziom, " Wybór: ", wybor,  " Podzbior: ", X,
          " PWybrane: ", PWybrane, " Suma wag: ", sumaWag)
    if(sumaWag == B):
        print(sumujWartość(X))
        return sumujWartość(X)
    if(sumaWag > B):
        return biezacyNajlepszy
    if(poziom == n):
        return sumujWartość(X)
    biezacyNajlepszy = sumujWartość(X)
    for i in range(0, n):
        if(PWybrane[i] == False):
            nowe = szukajRozwiazania(
                X[:], PWybrane[:], i, poziom+1, biezacyNajlepszy)
            if(biezacyNajlepszy < nowe):
                biezacyNajlepszy = nowe
    return biezacyNajlepszy


def sumujWagi(X):
    sum = 0
    for x in X:
        sum = sum+W[x]
    return sum


def sumujWartość(X):
    sum = 0
    for x in X:
        sum = sum + C[x]
    return sum


print("C:", C)
print("W:", W)
print("B:", B)


najlepszy = 0

for i in range(0, n):
    X = []
    for j in range(0, n):
        PoczatkoweWybrane[j] = False
    nowy = szukajRozwiazania(X, PoczatkoweWybrane, i, 0, 0)
    if(nowy > najlepszy):
        najlepszy = nowy

print(" Z maksimum: ", najlepszy)
