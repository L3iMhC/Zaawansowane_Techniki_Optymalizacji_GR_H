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

    def __repr__(self):
        return ("\nPoziom: "+str(self.poziom)+" Zysk do tej gałęzi: "+str(self.zyskDoTejGalezi)+" Waga do tej gałęzi: "+str(self.wagaDoTejGalezi)+" UB: "+str(self.UB)+" LB: "+str(self.LB)+" Wybrany: "+str(self.wybrany))


def losoweRozwPoczatkowe():
    Xp = []
    Pp = []
    for i in range(0, n):
        Pp.append(i)

    while Pp:
        wylosowany = random.choice(Pp)
        Xp.append(wylosowany)
        Pp.remove(wylosowany)
        if(sumujWagi(Xp) > B):
            Xp.remove(Xp[-1])
            return (Xp, sumujWartość(Xp))


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


def RozwiazBB():
    (Xp, LB) = losoweRozwPoczatkowe()
    nowag = obecnag = galaz(0, 0, 0, 0, False, 0)
    Q = []
    Q.append(galaz(-1, 0, 0, 0, False, 0))
    X = []
    itemsWiC = []
    maksymalnyZysk = 0
    for i in range(0, n):
        X.append(False)
        itemsWiC.append(itemWiC(W[i], C[i], i))
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


print("C:", C)
print("W:", W)
print("B:", B)

print(RozwiazBB())
