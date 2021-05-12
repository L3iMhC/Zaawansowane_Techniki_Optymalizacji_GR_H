from numpy.lib.function_base import diff
import generator as gen
import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt

moduleName = '../CPLEX/generator'


n = 50
Z = 4124
generator = gen.RandomNumberGenerator(Z)


p = np.zeros(n, dtype='int32')  # czas wykonania
w = np.zeros(n, dtype='int32')  # waga
d = np.zeros(n, dtype='int32')  # wymagany czas zakonczenia
S = 0
InitialQueue = np.zeros(n, dtype='int32')


def RandomSearch(queue, printMidPointValues=False):

    temp = queue
    BestQueue = queue
    BestLatency = WeightedLatency(queue)
    iterations = 0
    if(printMidPointValues):
        print('\n\n\n\nInitial queue: ', queue,
              '\nInitial latency: ', WeightedLatency(queue), '\n',)

    while(iterations < 1000):

        i1 = random.randint(0, n-1)
        i2 = random.randint(0, n-1)
        while(i1 == i2):
            i2 = random.randint(0, n-1)

        temp[i1], temp[i2] = temp[i2], temp[i1]
        CurrentLatency = WeightedLatency(temp)

        if(CurrentLatency < BestLatency):
            iterations = 0
            BestLatency = CurrentLatency
            BestQueue = temp.copy()
            if(printMidPointValues):
                print('\nCurrent Best Queue: ', BestQueue,
                      '\nCurrent Best Latency: ', BestLatency, '\n',)
        else:
            temp[i1], temp[i2] = temp[i2], temp[i1]
            iterations = iterations + 1

    return BestQueue, BestLatency


def acceptance(x1, x2, t):
    different = -(x1-x2)
    divided = different//t
    value = math.exp(divided)
    return value


def SimulatedAnnealing(n, queue, initialTemperature=1000, printMidPointValues=False):

    temp = queue
    BestLatency = WeightedLatency(queue)
    iterations = 0
    BestQueue = queue
    tmp = initialTemperature
    if(tmp < 100):
        finalTemp = 1
    else:
        finalTemp = initialTemperature/1000  # Final temp do dopasowania
    a = 0.95
    if(printMidPointValues):
        print('\n\n\n\nInitial queue: ', queue,
              '\nInitial value: ', WeightedLatency(queue), '\n',)
    startTime = time.time()

    i1 = 0
    i2 = n-1
    pr = n//5  # Promien w jakim szukamy sasiadow
    while(iterations < 10000):
        if(time.time()-startTime > 10 or tmp < 1/finalTemp or tmp < finalTemp):  # To trzba też dostosować
            break
        zi1 = i1  # Srodek zakresu w jakim szukamy i1
        zi2 = i2  # Srodek zakresu w jakim szukamy i2

        if(zi1-pr < 0):
            zi1 = zi1+pr
        if(zi1+pr > n-1):
            zi1 = zi1-pr
        if(zi2-pr < 0):
            zi2 = zi2+pr
        if(zi2+pr > n-1):
            zi2 = zi2-pr
        #print(i1, i2)
        i1 = random.randint(zi1-pr, zi1+pr)
        i2 = random.randint(zi2-pr, zi2+pr)
        while(i1 == i2):
            i2 = random.randint(zi2-pr, zi2+pr)
        PreviousValue = WeightedLatency(temp)
        temp[i1], temp[i2] = temp[i2], temp[i1]
        CurrentValue = WeightedLatency(temp)

        if(CurrentValue < BestLatency):
            iterations = 0
            BestLatency = CurrentValue
            BestQueue = temp.copy()
            if(printMidPointValues):
                print('\nCurrent Best queue: ', BestQueue,
                      '\nCurrent Best value: ', BestLatency, '\n',)
        elif(random.random() < acceptance(PreviousValue, CurrentValue, tmp)):
            iterations = 0
        else:
            temp[i1], temp[i2] = temp[i2], temp[i1]
            iterations = iterations + 1

        tmp = a*tmp

    return BestQueue, BestLatency


def FindInitialTemperature(initialQueue):
    Lowest = 999999999999999
    Highest = 0
    for i in range(0, 10000):
        current = WeightedLatency(initialQueue)
        if current < Lowest:
            Lowest = current
        if current > Highest:
            Highest = current

        np.random.shuffle(initialQueue)
        # print(initialQueue)

    return abs(Highest-Lowest)


for i in range(0, n):
    InitialQueue[i] = i
    p[i] = generator.nextInt(1, 30)
    w[i] = generator.nextInt(1, 30)
    S += p[i]
for i in range(0, n):
    d[i] = generator.nextInt(1, S)

np.random.shuffle(InitialQueue)  # losowe rozwiazanie poczatkowe


def WeightedLatency(queue):
    C = np.zeros(n, dtype='long')
    T = np.zeros(n, dtype='long')
    C[queue[0]] = p[queue[0]]
    for i in range(1, n):
        C[queue[i]] = C[queue[i-1]]+p[queue[i]]
    for i in range(0, n):
        T[queue[i]] = max(0, C[queue[i]] - d[queue[i]])
    return (w*T).sum()


MaxWielkoscInstancji = 50
MinWielkoscInstancji = 10
RSValues = []
RSTimes = []
SAValues = []
SATimes = []
InitialValues = []
for n in range(MinWielkoscInstancji, MaxWielkoscInstancji):
    print(n)
    p = np.zeros(n, dtype='int32')  # czas wykonania
    w = np.zeros(n, dtype='int32')  # waga
    d = np.zeros(n, dtype='int32')  # wymagany czas zakonczenia
    S = 0
    InitialQueue = np.zeros(n, dtype='int32')
    for j in range(0, n):
        InitialQueue[j] = j
        p[j] = generator.nextInt(1, 30)
        w[j] = generator.nextInt(1, 30)
        S += p[j]
    for j in range(0, n):
        d[j] = generator.nextInt(1, S)

    np.random.shuffle(InitialQueue)  # losowe rozwiazanie poczatkowe
    InitialLatency = WeightedLatency(InitialQueue.copy())
    InitialValues.append(InitialLatency)
    # print('Initial queue: ', InitialQueue,
    #       '\nInitial latency: ', InitialLatency)

    startTime = time.time()
    RandomSearchBestQueue, RandomSearchBestLatency = RandomSearch(
        InitialQueue.copy())
    endTime = time.time()
    RSTimes.append(endTime-startTime)
    RSValues.append(RandomSearchBestLatency)

    # print('\n\n\n\n(RS)Final queue: ', RandomSearchBestQueue,
    #       '\n(RS)Final latency: ', RandomSearchBestLatency)

    initTemp = FindInitialTemperature(InitialQueue.copy())
    if(initTemp == 0):
        initTemp = 1000

    startTime = time.time()
    SimulatedAnnealingBestQueue, SimulatedAnnealingBestLatency = SimulatedAnnealing(n,
                                                                                    queue=InitialQueue.copy(), initialTemperature=initTemp)
    endTime = time.time()
    SATimes.append(endTime-startTime)
    SAValues.append(SimulatedAnnealingBestLatency)
    # print('\n\n\n\n(SA)Final queue: ', SimulatedAnnealingBestQueue,
    #       '\n(SA)Final latency: ', SimulatedAnnealingBestLatency)

x = np.arange(MinWielkoscInstancji, MaxWielkoscInstancji)
plt.title("Czas minimalizacji problemu witi na jednej maszynie w zależności od wielkości instancji")
plt.xlabel("Liczba zmiennych")
plt.ylabel("Czas rozwiązywania")
plt.plot(x, RSTimes, "o", label="Random Search")
plt.plot(x, SATimes, "o", label="Symulowane wyżarzanie")
plt.legend()
plt.show()

plt.title("Znaleziona wartość minimalna problemu witi na jednej maszynie w zależności od wielkości instancji")
plt.xlabel("Liczba zmiennych")
plt.ylabel("Wartosc rozwiązywania")
plt.plot(x, RSValues, "o", label="Random Search")
plt.plot(x, SAValues, "o", label="Symulowane wyżarzanie")
plt.plot(x, InitialValues, "o", label="Wartość początkowa")
plt.legend()
plt.show()
