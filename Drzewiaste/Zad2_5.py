import generator as gen
import numpy as np

moduleName = '../CPLEX/generator'

n = 6
Z = 4124
generator = gen.RandomNumberGenerator(Z)

X = []
PoczatkoweWybrane = []

C = np.zeros(n)
W = np.zeros(n)
B = generator.nextInt(5*n, 10*n)
for i in range(0, n):
    C[i] = generator.nextInt(1, 30)
    W[i] = generator.nextInt(1, 30)
    PoczatkoweWybrane.append(False)

# BRUTE FORCE


def szukajRozwiazania(X, PWybrane, wybor, poziom, biezacyNajlepszy, limitGlebokosci=0):

    PWybrane[wybor] = True
    X.append(wybor)
    sumaWag = sumujWagi(X)

    if(sumaWag == B):
        print("Suma wag rowna wadze ograniczajacej z suma wartosci: ", sumujWartość(X))
        return sumujWartość(X)
    if(sumaWag > B):
        #PWybrane[wybor] = False
        # X.remove(wybor)
        return biezacyNajlepszy
    if(poziom == n):
        return sumujWartość(X)
    biezacyNajlepszy = sumujWartość(X)
    print("Poziom: ", poziom, " Wybór: ", wybor,  " Podzbior: ", X,
          " PWybrane: ", PWybrane, " Suma wag: ", sumaWag, " Bieżący najlepszy: ", biezacyNajlepszy)
    for k in range(0, n):
        if(PWybrane[k] == False):
            nowe = szukajRozwiazania(
                X[:], PWybrane[:], k, poziom+1, biezacyNajlepszy)
            if(biezacyNajlepszy < nowe):
                biezacyNajlepszy = nowe
    return biezacyNajlepszy


X = []
PStart = []
for i in range(0, n):
    PStart.append(False)


def szukajRozwiazaniaTest(X, P, wybor, poziom):
    P[wybor] = True
    X.append(wybor)
    print("P: ", P, " Wybor: ", wybor, " X: ", X)
    for item in range(0, n):
        #print(poziom, ".", item, " P: ", P)
        if(P[item] == False):
            szukajRozwiazaniaTest(X[:], P[:], item, poziom+1)
            P[item] = True


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
    #PoczatkoweWybrane[i] = False
    for j in range(0, n):
        PoczatkoweWybrane[j] = False
    nowy = szukajRozwiazania(X[:], PoczatkoweWybrane[:], i, 0, 0)
    if(nowy > najlepszy):
        najlepszy = nowy

print(" Z maksimum: ", najlepszy)
