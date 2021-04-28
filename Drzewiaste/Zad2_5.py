import generator as gen
import numpy as np
import random

moduleName = '../CPLEX/generator'

n = 5
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

#print(LiczProblemPlecakowy(B, W, C, n))

# This code is contributed by Nikhil Kumar Singh


# Podejscie Greediego w sortowaniu kosztow

# A simple implementation of Priority Queue
# using Queue.
class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()


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

    def __str__(self):
        return ("Waga: ", self.waga, " Wartosc: ", self.wartosc, " ID: ", self.id)

    def __repr__(self):
        return ("\nWaga: " + str(self.waga) + " Wartosc: " + str(self.wartosc) + " ID: "+str(self.id))


class galaz:
    def __init__(self, poziom, zyskDoTejGalezi, UB, LB, Wybrany, wagaDoTejGalezi):
        self.poziom = poziom
        self.zyskDoTejGalezi = zyskDoTejGalezi
        self.UB = UB
        self.LB = LB
        self.wagaDoTejGalezi = wagaDoTejGalezi
        self.wybrany = Wybrany

    def __lt__(self, other):
        return self.LB > other.LB


def znajdzGorneOgraniczenie(zyskDoTejGalezi, wagaDoTejGalezi, id, itemsWiC):
    wartosc = zyskDoTejGalezi
    waga = wagaDoTejGalezi
    for i in range(id, n):
        if waga+itemsWiC[i].waga <= B:
            waga = waga + itemsWiC[i].waga
            wartosc = wartosc - itemsWiC[i].wartosc
        else:
            wartosc = wartosc - (B-waga)/itemsWiC[i].waga*itemsWiC[i].wartosc
            break
    return wartosc


def znajdzDolneOgraniczenie(zyskDoTejGalezi, wagaDoTejGalezi, id, itemsWiC):
    wartosc = zyskDoTejGalezi
    waga = wagaDoTejGalezi
    for i in range(id, n):
        if waga+itemsWiC[i].waga <= B:
            waga += itemsWiC[i].waga
            wartosc -= itemsWiC[i].wartosc
        else:
            break
    return wartosc


def przypiszGaleziWartosci(Galaz, UB, LB, poziom, Wybrany, zyskDoTejGalezi, wagaDoTejGalezi):
    Galaz.poziom = poziom
    Galaz.zyskDoTejGalezi = zyskDoTejGalezi
    Galaz.UB = UB
    Galaz.LB = LB
    Galaz.wagaDoTejGalezi = wagaDoTejGalezi
    Galaz.wybrany = Wybrany


def znajdzMaksimumPlecaka(Wartosci, Wagi):
    itemWiCs = []
    minLB = 0
    # wartość lowerbound na lisciach w drzewie
    ostateczneLB = 9999999999999999999999999
    biezacaSciezka = []
    ostatecznaSciezka = []
    biezacaGalaz = lewaGalaz = prawaGalaz = galaz(0, 0, 0, 0, False, 0)
    for i in range(0, n):
        itemWiCs.append(itemWiC(Wagi[i], Wartosci[i], i))
        ostatecznaSciezka.append(False)
        biezacaSciezka.append(False)
    print(itemWiCs)
    itemWiCs.sort(reverse=True)

    Q = PriorityQueue()
    Q.insert(biezacaGalaz)
    z = 0
    while not Q.isEmpty():
        z += 1

        biezacaGalaz = Q.delete()
        print(biezacaGalaz.UB, minLB)
        if(biezacaGalaz.UB > minLB or biezacaGalaz.UB >= ostateczneLB):
            continue

        if(biezacaGalaz.poziom != 0):
            biezacaSciezka[biezacaGalaz.poziom - 1] = biezacaGalaz.wybrany

        if(biezacaGalaz.poziom == n-1):
            if(biezacaGalaz.LB < ostateczneLB):
                for i in range(0, n):
                    ostatecznaSciezka[itemWiCs[i].id] = biezacaSciezka[i]
            print(ostateczneLB)
            ostateczneLB = min(biezacaGalaz.LB, ostateczneLB)
            continue

        poziom = biezacaGalaz.poziom

        przypiszGaleziWartosci(prawaGalaz,
                               znajdzGorneOgraniczenie(
                                   biezacaGalaz.zyskDoTejGalezi, biezacaGalaz.wagaDoTejGalezi, poziom+1, itemWiCs),
                               znajdzDolneOgraniczenie(
                                   biezacaGalaz.zyskDoTejGalezi, biezacaGalaz.wagaDoTejGalezi, poziom+1, itemWiCs),
                               poziom+1, False, biezacaGalaz.zyskDoTejGalezi, biezacaGalaz.wagaDoTejGalezi)

        if(biezacaGalaz.wagaDoTejGalezi + itemWiCs[biezacaGalaz.poziom].waga <= B):
            lewaGalaz.UB = znajdzGorneOgraniczenie(
                biezacaGalaz.zyskDoTejGalezi - itemWiCs[poziom].wartosc, biezacaGalaz.wagaDoTejGalezi + itemWiCs[poziom].waga, poziom+1, itemWiCs)
            lewaGalaz.LB = znajdzDolneOgraniczenie(
                biezacaGalaz.zyskDoTejGalezi - itemWiCs[poziom].wartosc, biezacaGalaz.wagaDoTejGalezi + itemWiCs[poziom].waga, poziom+1, itemWiCs)
            przypiszGaleziWartosci(lewaGalaz, lewaGalaz.UB, lewaGalaz.LB, poziom+1, True, biezacaGalaz.zyskDoTejGalezi -
                                   itemWiCs[poziom].wartosc, biezacaGalaz.wagaDoTejGalezi + itemWiCs[poziom].waga)

        else:
            lewaGalaz.UB = lewaGalaz.LB = 1

        minLB = min(minLB, lewaGalaz.LB)
        minLB = min(minLB, prawaGalaz.LB)
        if(minLB >= lewaGalaz.UB):
            Q.insert(lewaGalaz)
        if(minLB >= prawaGalaz.UB):
            Q.insert(prawaGalaz)

    print("Znaleziono maksymalna wartosc: ", ostateczneLB,
          " Dla wyborow: ", ostatecznaSciezka)


znajdzMaksimumPlecaka(C, W)
