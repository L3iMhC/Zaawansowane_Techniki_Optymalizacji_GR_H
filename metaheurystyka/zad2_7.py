import generator as gen
import numpy as np
import random
import math
import time

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
    value = pow(math.e, (-(x1-x2)/t))
    return value


def SimulatedAnnealing(queue, initialTemperature=1000, printMidPointValues=False):

    temp = queue
    BestLatency = WeightedLatency(queue)
    iterations = 0

    tmp = initialTemperature
    a = 0.995
    if(printMidPointValues):
        print('\n\n\n\nInitial queue: ', queue,
              '\nInitial value: ', WeightedLatency(queue), '\n',)
    startTime = time.time()
    while(iterations < 10000):
        if(time.time()-startTime > 10):
            break
        i1 = random.randint(0, n-1)
        i2 = random.randint(0, n-1)
        while(i1 == i2):
            i2 = random.randint(0, n-1)

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
    C = np.zeros(n, dtype='int32')
    T = np.zeros(n, dtype='int32')
    C[queue[0]] = p[queue[0]]
    for i in range(1, n):
        C[queue[i]] = C[queue[i-1]]+p[queue[i]]
    for i in range(0, n):
        T[queue[i]] = max(0, C[queue[i]] - d[queue[i]])
    return (w*T).sum()


InitialLatency = WeightedLatency(InitialQueue.copy())

print('Initial queue: ', InitialQueue, '\nInitial latency: ', InitialLatency)

RandomSearchBestQueue, RandomSearchBestLatency = RandomSearch(
    InitialQueue.copy())

print('\n\n\n\n(RS)Final queue: ', RandomSearchBestQueue,
      '\n(RS)Final latency: ', RandomSearchBestLatency)

initTemp = FindInitialTemperature(InitialQueue.copy())
if(initTemp == 0):
    initTemp = 1000
print(initTemp)
SimulatedAnnealingBestQueue, SimulatedAnnealingBestLatency = SimulatedAnnealing(
    queue=InitialQueue.copy(), initialTemperature=initTemp)

print('\n\n\n\n(SA)Final queue: ', SimulatedAnnealingBestQueue,
      '\n(SA)Final latency: ', SimulatedAnnealingBestLatency)
