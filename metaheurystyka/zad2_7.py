import generator as gen
import numpy as np
import random
import math

moduleName = '../CPLEX/generator'


n = 5
Z = 4124
generator = gen.RandomNumberGenerator(Z)


p = np.zeros(n, dtype='int32') #czas wykonania
w = np.zeros(n, dtype='int32') #waga
d = np.zeros(n, dtype='int32') #wymagany czas zakonczenia
S=0
InitialQueue = np.zeros(n, dtype='int32')

for i in range(0, n):
    InitialQueue[i] = i
    p[i] = generator.nextInt(1, 30)
    w[i] = generator.nextInt(1, 30)
    S+=p[i]
for i in range(0, n):
    d[i] = generator.nextInt(1, S)

np.random.shuffle(InitialQueue) #losowe rozwiazanie poczatkowe

def WeightedLatency(queue):
    C = np.zeros(n, dtype='int32')
    T = np.zeros(n, dtype='int32')
    C[queue[0]] = p[queue[0]]
    for i in range(1, n):
        C[queue[i]] = C[queue[i-1]]+p[queue[i]]
    for i in range(0, n):
        T[queue[i]] = max(0, C[queue[i]] - d[queue[i]])
    return w*T


InitialLatency = WeightedLatency(InitialQueue.copy())

print('Initial Path: ',InitialQueue,'\nInitial Distance: ',InitialLatency)
