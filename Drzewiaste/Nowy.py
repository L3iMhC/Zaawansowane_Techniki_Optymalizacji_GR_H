import generator as gen
import numpy as np
import datetime
from matplotlib import pyplot as plt

moduleName = '../CPLEX/generator'


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
        return ("\nWaga: " + str(self.waga) + " Wartosc: " + str(self.wartosc) + " ID: "+str(self.id)+" Koszt: "+str(self.koszt))


class galaz:
    def __init__(self, poziom, zyskDoTejGalezi, UB, LB, Wybrany, wagaDoTejGalezi):
        self.poziom = poziom
        self.zyskDoTejGalezi = zyskDoTejGalezi
        self.UB = UB
        self.wagaDoTejGalezi = wagaDoTejGalezi

    def __repr__(self):
        return ("\nPoziom: "+str(self.poziom)+" Zysk do tej gałęzi: "+str(self.zyskDoTejGalezi)+" Waga do tej gałęzi: "+str(self.wagaDoTejGalezi)+" UB: "+str(self.UB)+" LB: "+str(self.LB)+" Wybrany: "+str(self.wybrany))


def liczUB(galaz, itemsWiC):
    if(galaz.wagaDoTejGalezi >= B):
        return 0
    UB = galaz.zyskDoTejGalezi
    j = galaz.poziom + 1
    SumaWag = galaz.wagaDoTejGalezi

    while((j < n) and (SumaWag + itemsWiC[j].waga <= B)):
        SumaWag += itemsWiC[j].waga
        UB += itemsWiC[j].wartosc
        j += 1

    if j < n:
        UB += (B-SumaWag)*itemsWiC[j].wartosc/itemsWiC[j].waga
    return UB


def RozwiazBF(B, n):
    if n == 0 or B == 0:
        return 0
    if(W[n-1] > B):
        return RozwiazBF(B, n-1)
    else:
        return max(C[n-1] + RozwiazBF(B-W[n-1], n-1), RozwiazBF(B, n-1))


def RozwiazBB(zSortowaniem):
    nowag = obecnag = galaz(0, 0, 0, 0, False, 0)
    Q = []
    Q.append(galaz(-1, 0, 0, 0, False, 0))
    X = []
    itemsWiC = []
    maksymalnyZysk = 0
    for i in range(0, n):
        X.append(False)
        itemsWiC.append(itemWiC(W[i], C[i], i))
    if(zSortowaniem):
        itemsWiC.sort(reverse=False)
    print(itemsWiC)
    while len(Q) != 0:
        obecnag = Q.pop()
        if(obecnag.poziom == -1):
            nowag.poziom = 0
        if(obecnag.poziom == n-1):
            continue
        nowag.poziom = obecnag.poziom + 1
        nowag.wagaDoTejGalezi = obecnag.wagaDoTejGalezi + \
            itemsWiC[nowag.poziom].waga
        nowag.zyskDoTejGalezi = obecnag.zyskDoTejGalezi + \
            itemsWiC[nowag.poziom].wartosc

        if(nowag.wagaDoTejGalezi <= B and nowag.zyskDoTejGalezi > maksymalnyZysk):
            maksymalnyZysk = nowag.zyskDoTejGalezi

        nowag.UB = liczUB(nowag, itemsWiC)

        if(nowag.UB > maksymalnyZysk):
            Q.append(nowag)

        nowag.wagaDoTejGalezi = obecnag.wagaDoTejGalezi
        nowag.zyskDoTejGalezi = obecnag.zyskDoTejGalezi
        nowag.UB = liczUB(nowag, itemsWiC)
        if(nowag.UB > maksymalnyZysk):
            Q.append(nowag)

    return maksymalnyZysk


BF = []
BBzSortowaniem = []
BBbezSortowania = []


wielkoscInstancji = 25
for i in range(0, wielkoscInstancji):
    n = i
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

    print("C:", C)
    print("W:", W)
    print("B:", B)
    start = datetime.datetime.now()
    BBbezSortowania.append(RozwiazBB(False))
    duration = datetime.datetime.now() - start
    start = datetime.datetime.now()
    BBzSortowaniem.append(RozwiazBB(True))
    duration = datetime.datetime.now() - start
    start = datetime.datetime.now()
    BF.append(RozwiazBF(B, n))
    duration = datetime.datetime.now() - start

x = np.arange(0, wielkoscInstancji)
plt.title("Czas maksymalizacji problemu plecakowego algorytmu B&B w porównaniu do Brute Force w zależności od liczby zmiennych")
plt.xlabel("Liczba zmiennych")
plt.ylabel("Czas rozwiązywania")
plt.plot(x, BBbezSortowania, "o", label="B&B bez sortowania")
plt.plot(x, BBzSortowaniem, "o", label="B&B z sortowaniem")
plt.plot(x, BF, "o", label="Brute Force")
plt.legend()
plt.show()
