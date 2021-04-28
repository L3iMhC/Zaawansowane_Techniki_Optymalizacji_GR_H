import generator as gen
import numpy as np
import random

moduleName = '../CPLEX/generator'

n = 25
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

# # BRUTE FORCE


# def szukajRozwiazania(X, PWybrane, wybor, poziom=0, biezacyNajlepszy=0, najlepszaPermutacja=0, limitGlebokosci=0):

#     PWybrane[wybor] = True
#     X.append(wybor)
#     sumaWag = sumujWagi(X)
#     if(sumaWag == B):
#         #print("Suma wag rowna wadze ograniczajacej z suma wartosci: ", sumujWartość(X))
#         return (X, sumujWartość(X))
#     if(sumaWag > B):
#         #PWybrane[wybor] = False
#         # X.remove(wybor)
#         return (najlepszaPermutacja, biezacyNajlepszy)
#     if(poziom == n):
#         return (X, sumujWartość(X))
#     biezacyNajlepszy = sumujWartość(X)
#     najlepszaPermutacja = X
#     # print("Poziom: ", poziom, " Wybór: ", wybor,  " Podzbior: ", X,
#     #      " PWybrane: ", PWybrane, " Suma wag: ", sumaWag, " Bieżący najlepszy: ", biezacyNajlepszy)
#     for k in range(0, n):
#         if(PWybrane[k] == False):
#             (nowaPermutacja, nowe) = szukajRozwiazania(
#                 X[:], PWybrane[:], k, poziom+1, biezacyNajlepszy, najlepszaPermutacja)
#             if(biezacyNajlepszy < nowe):
#                 biezacyNajlepszy = nowe
#                 najlepszaPermutacja = nowaPermutacja
#     return (najlepszaPermutacja, biezacyNajlepszy)


# def losoweRozwPoczatkowe():
#     Xp = []
#     Pp = []
#     for i in range(0, n):
#         Pp.append(i)

#     while Pp:
#         wylosowany = random.choice(Pp)
#         Xp.append(wylosowany)
#         Pp.remove(wylosowany)
#         if(sumujWagi(Xp) > B):
#             Xp.remove(Xp[-1])
#             return (Xp, sumujWartość(Xp))


# X = []
# PStart = []
# for i in range(0, n):
#     PStart.append(False)


# def szukajRozwiazaniaTest(X, P, wybor, poziom):
#     P[wybor] = True
#     X.append(wybor)
#     print("P: ", P, " Wybor: ", wybor, " X: ", X)
#     for item in range(0, n):
#         #print(poziom, ".", item, " P: ", P)
#         if(P[item] == False):
#             szukajRozwiazaniaTest(X[:], P[:], item, poziom+1)
#             P[item] = True


# def sumujWagi(X):
#     sum = 0
#     for x in X:
#         sum = sum+W[x]
#     return sum


# def sumujWartość(X):
#     sum = 0
#     for x in X:
#         sum = sum + C[x]
#     return sum


print("C:", C)
print("W:", W)
print("B:", B)


# najlepszy = 0
# najlepszaPermutacja = []

# (permutacjaLosowa, LB) = losoweRozwPoczatkowe()
# print("LB: ", LB, " Dla: ", permutacjaLosowa)
# for i in range(0, n):
#     X = []
#     #PoczatkoweWybrane[i] = False
#     for j in range(i, n):
#         PoczatkoweWybrane[j] = False
#     (nowaPermutacja, nowy) = szukajRozwiazania(
#         X[:], PoczatkoweWybrane[:], i)
#     if(nowy > najlepszy):
#         najlepszy = nowy
#         najlepszaPermutacja = nowaPermutacja

# print("Najlepsza permutacja: ", najlepszaPermutacja, " Z maksimum: ", najlepszy)


# WERSJA HINDUSKA LC-BB
# X = []
# # Jeśli jedynka to go wybieramy, tzn pakujemy do plecaka xD Na początku kradniemy wszystko
# for i in range(0, n):
#     X[i] = 1


# def liczGorneOgraniczenie(X):
#     sumaWartosci = 0
#     sumaWag = 0
#     for i in range(0, n):
#         if(X[i] != 0):
#             sumaWartosci = sumaWartosci+C[i]
#             sumaWag = sumaWag+W[i]
#             if(i == n):
#                 return (-1)*sumaWartosci


# def liczKoszt(X):
#     sumaWartosci = 0
#     sumaWag = 0
#     for i in range(0, n):
#         if(X[i] != 0):
#             sumaWartosci = sumaWartosci+C[i]
#             sumaWag = sumaWag+W[i]
#             if(i == n):
#                 return (-1)*(sumaWartosci+(C[i]/W[i]*(B-sumaWag)))


# for i in range(0, n):
#     X[i]=0


# A naive recursive implementation
# of 0-1 Knapsack Problem

# Returns the maximum value that
# can be put in a knapsack of
# capacity W


def LiczProblemPlecakowy(Ograniczenie, Wagi, Wartosci, Poziom):

    # Base Case
    if (Poziom == 0 or Ograniczenie == 0):
        return 0

    # If weight of the nth item is
    # more than Knapsack of capacity W,
    # then this item cannot be included
    # in the optimal solution
    if (Wagi[Poziom-1] > Ograniczenie):
        return LiczProblemPlecakowy(Ograniczenie, Wagi, Wartosci, Poziom-1)

    # return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(
            Wartosci[Poziom-1] + LiczProblemPlecakowy(
                Ograniczenie-Wagi[Poziom-1], Wagi, Wartosci, Poziom-1),
            LiczProblemPlecakowy(Ograniczenie, Wagi, Wartosci, Poziom-1))

# end of function knapSack


# Driver Code

print(LiczProblemPlecakowy(B, W, C, n))

# This code is contributed by Nikhil Kumar Singh


# Podejscie Greediego
class itemWiC:
    def __init__(self, waga, wartosc, id):
        self.waga = waga
        self.wartosc = wartosc
        self.id = id
        if(wartosc != 0 and waga != 0):
            self.koszt = wartosc//waga
        else:
            self.koszt = 0

    def __lt__(self, other):
        return self.koszt < other.koszt


def znajdzMaksimumPlecaka(Wartosci, Wagi, MaksymalnaPojemnoscPlecaka):
    itemWiCs = []
    for i in range(0, n):
        itemWiCs.append(itemWiC(Wagi[i], Wartosci[i], i))

    itemWiCs.sort(reverse=True)
    maxZysk = 0
    Q = []
    Q.append(itemWiC(0, 0, n))


znajdzMaksimumPlecaka(C, W, B)
