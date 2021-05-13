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


def RandomSearch(n, queue, printMidPointValues=False, neighborhood='Other'):

    temp = queue
    BestQueue = queue
    BestLatency = WeightedLatency(queue)
    iterations = 0
    if(printMidPointValues):
        print('\n\n\n\nInitial queue: ', queue,
              '\nInitial latency: ', WeightedLatency(queue), '\n',)
    if(neighborhood=='Other'):
        i1 = 0
        i2 = n-1
        pr = n//5  # Promien w jakim szukamy sasiadow
    while(iterations < 10000):

        if(neighborhood=='Other'):
            temp, i1, i2 = OtherNeighborhood(i1, i2, pr, n, temp)
        elif(neighborhood=='Rand'):
            temp, i1, i2 = RandomNeighborhood(n, temp)
        else:
            print('No zly parametr sasiedztwa')

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


def SimulatedAnnealing(n, queue, initialTemperature=1000, printMidPointValues=False, neighborhood='Other'):

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

    if(neighborhood=='Other'):
        i1 = 0
        i2 = n-1
        pr = n//5  # Promien w jakim szukamy sasiadow
    while(iterations < 10000):
        if(time.time()-startTime > 10 or tmp < 1/finalTemp or tmp < finalTemp):  # To trzba też dostosować
            break

        PreviousValue = WeightedLatency(temp)

        if(neighborhood=='Other'):
            temp, i1, i2 = OtherNeighborhood(i1, i2, pr, n, temp)
        elif(neighborhood=='Rand'):
            temp, i1, i2 = RandomNeighborhood(n, temp)
        else:
            print('No zly parametr sasiedztwa')

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

def RandomNeighborhood(n, temp):
    i1 = random.randint(0, n-1)
    i2 = random.randint(0, n-1)
    while(i1 == i2):
        i2 = random.randint(0, n-1)
    temp[i1], temp[i2] = temp[i2], temp[i1]
    return temp, i1, i2

def OtherNeighborhood(i1, i2, pr, n, temp):
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
    temp[i1], temp[i2] = temp[i2], temp[i1]

    return temp, i1, i2

MaxWielkoscInstancji = 50
MinWielkoscInstancji = 10
RS1Values = []#Sasiedztwo OtherNeigborhood
RS1Times = []
RS2Values = []#Sasiedztwo RandomNeighborhood
RS2Times = []
SA1Values = []#Sasiedztwo OtherNeigborhood
SA1Times = []
SA2Values = []#Sasiedztwo RandomNeighborhood
SA2Times = []
InitialValues = []

for n in range(MinWielkoscInstancji, MaxWielkoscInstancji):
    print(n)
    InitialQueues = []

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
    
    BestLatency = 9999999999
    for i in range(0, 100):
        np.random.shuffle(InitialQueue)
        InitialQueues.append(InitialQueue.copy())  # losowe rozwiazanie poczatkowe
    for i in range(0, 100):
        CurrentLatency = WeightedLatency(InitialQueues[i])
        if(CurrentLatency<BestLatency):
            BestLatency = CurrentLatency
            InitialQueue = InitialQueues[i]

    InitialLatency = WeightedLatency(InitialQueue.copy())
    InitialValues.append(InitialLatency)
    #print('Initial queue: ', InitialQueue,
     #      '\nInitial latency: ', InitialLatency)

    startTime = time.time()
    RandomSearchBestQueue, RandomSearchBestLatency = RandomSearch(
        n, InitialQueue.copy())
    endTime = time.time()
    RS1Times.append(endTime-startTime)
    RS1Values.append(RandomSearchBestLatency)

    #Random Neighborhood
    startTime = time.time()
    RandomSearchBestQueue, RandomSearchBestLatency = RandomSearch(
        n, InitialQueue.copy(),neighborhood='Rand')
    endTime = time.time()
    RS2Times.append(endTime-startTime)
    RS2Values.append(RandomSearchBestLatency)
    # print('\n\n\n\n(RS)Final queue: ', RandomSearchBestQueue,
    #       '\n(RS)Final latency: ', RandomSearchBestLatency)

    initTemp = FindInitialTemperature(InitialQueue.copy())
    if(initTemp == 0):
        initTemp = 1000

    startTime = time.time()
    SimulatedAnnealingBestQueue, SimulatedAnnealingBestLatency = SimulatedAnnealing(n,
                                                                                    queue=InitialQueue.copy(), initialTemperature=initTemp)
    endTime = time.time()
    SA1Times.append(endTime-startTime)
    SA1Values.append(SimulatedAnnealingBestLatency)

    #Random Neighborhood
    startTime = time.time()
    SimulatedAnnealingBestQueue, SimulatedAnnealingBestLatency = SimulatedAnnealing(n,
                                                                                    queue=InitialQueue.copy(), initialTemperature=initTemp, neighborhood='Rand')
    endTime = time.time()
    SA2Times.append(endTime-startTime)
    SA2Values.append(SimulatedAnnealingBestLatency)
    # print('\n\n\n\n(SA)Final queue: ', SimulatedAnnealingBestQueue,
    #       '\n(SA)Final latency: ', SimulatedAnnealingBestLatency)

x = np.arange(MinWielkoscInstancji, MaxWielkoscInstancji)
plt.title("Czas minimalizacji problemu witi na jednej maszynie w zależności od wielkości instancji")
plt.xlabel("Liczba zmiennych")
plt.ylabel("Czas rozwiązywania")
plt.plot(x, RS1Times, "o", label="Random Search Sasiedztwo")
plt.plot(x, RS2Times, "o", label="Random Search Losowe")
plt.plot(x, SA1Times, "o", label="Symulowane wyżarzanie Sasiedztwo")
plt.plot(x, SA2Times, "o", label="Symulowane wyżarzanie Losowe")
plt.legend()
plt.show()

plt.title("Znaleziona wartość minimalna problemu witi na jednej maszynie w zależności od wielkości instancji")
plt.xlabel("Liczba zmiennych")
plt.ylabel("Wartosc rozwiązywania")
plt.plot(x, RS1Values, "o", label="Random Search Sasiedztwo")
plt.plot(x, RS2Values, "o", label="Random Search Losowe")
plt.plot(x, SA1Values, "o", label="Symulowane wyżarzanie Sasiedztwo")
plt.plot(x, SA2Values, "o", label="Symulowane wyżarzanie Losowe")
plt.plot(x, InitialValues, "o", label="Wartość początkowa")
plt.legend()
plt.show()
