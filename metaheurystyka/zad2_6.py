import generator as gen
import numpy as np
import random

moduleName = '../CPLEX/generator'

n = 5
Z = 4124
generator = gen.RandomNumberGenerator(Z)


d = np.zeros((n, n), dtype='int32') #dystanse miast
InitialPath = np.zeros(n, dtype='int32')
for i in range(0, n):
    InitialPath[i] = i
    for j in range(0, n):
        d[i][j] = generator.nextInt(1, 30)

np.random.shuffle(InitialPath) #losowe rozwiazanie poczatkowe



def WholeDistance(path):
    sum=0
    for i in range(0, n-1):
        sum+=d[path[i], path[i+1]]
    sum+=d[path[0], path[n-1]]
    return sum















print(InitialPath)

FinalDistance = WholeDistance(InitialPath)

print(FinalDistance)