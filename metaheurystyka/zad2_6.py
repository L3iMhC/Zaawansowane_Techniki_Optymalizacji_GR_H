import generator as gen
import numpy as np
import random
import math

moduleName = '../CPLEX/generator'

def WholeDistance(path):
    sum=0
    for i in range(0, n-1):
        sum+=d[path[i], path[i+1]]
    sum+=d[path[n-1], path[0]]
    return sum


def RandomSearch(path):

    temp = path
    BestDistance = WholeDistance(path)
    iterations=0

    print('\n\n\n\nInitial Path: ',path, '\nInitial Distance: ',WholeDistance(path), '\n',)

    while(iterations<1000):
        
        i1 = random.randint(0,n-1)
        i2 = random.randint(0,n-1)
        while(i1==i2):
            i2 = random.randint(0,n-1)

        temp[i1], temp[i2] = temp[i2], temp[i1]
        CurrentDistance = WholeDistance(temp)

        if(CurrentDistance<BestDistance):
            iterations=0
            BestDistance=CurrentDistance
            BestPath = temp.copy()
            print('\nCurrent Best Path: ',BestPath, '\nCurrent Best Distance: ',BestDistance, '\n',)
        else:
            temp[i1], temp[i2] = temp[i2], temp[i1]
            iterations = iterations +1

    return BestPath, BestDistance

def acceptance(x1, x2, t):
    return math.e**(-(x1-x2)/t)



def SimulatedAnnealing(path):

    temp = path
    BestDistance = WholeDistance(path)
    iterations=0


    tmp = 1000
    a = 0.995

    print('\n\n\n\nInitial Path: ',path, '\nInitial Distance: ',WholeDistance(path), '\n',)

    while(iterations<10000):
        
        i1 = random.randint(0,n-1)
        i2 = random.randint(0,n-1)
        while(i1==i2):
            i2 = random.randint(0,n-1)

        PreviousDistance = WholeDistance(temp)
        temp[i1], temp[i2] = temp[i2], temp[i1]
        CurrentDistance = WholeDistance(temp)

        if(CurrentDistance<BestDistance):
            iterations=0
            BestDistance=CurrentDistance
            BestPath = temp.copy()
            print('\nCurrent Best Path: ',BestPath, '\nCurrent Best Distance: ',BestDistance, '\n',)
        elif(random.random()<acceptance(PreviousDistance,CurrentDistance,tmp)):
            iterations=0
        else:
            temp[i1], temp[i2] = temp[i2], temp[i1]
            iterations = iterations + 1

        tmp=a*tmp

    return BestPath, BestDistance



n = 20
Z = 4124
generator = gen.RandomNumberGenerator(Z)


d = np.zeros((n, n), dtype='int32') #dystanse miast
InitialPath = np.zeros(n, dtype='int32')
for i in range(0, n):
    InitialPath[i] = i
    for j in range(0, n):
        d[i][j] = generator.nextInt(1, 30)
    d[i][i] = 0

np.random.shuffle(InitialPath) #losowe rozwiazanie poczatkowe





InitialDistance = WholeDistance(InitialPath)

print('Initial Path: ',InitialPath,'\nInitial Distance: ',InitialDistance)

FinalPathRS, FinalDistanceRS = RandomSearch(path = InitialPath.copy())

print('\n\n\n\n(RS)Final Path: ',FinalPathRS,'\n(RS)Final Distance: ',FinalDistanceRS, '\n\nDistances:\n',d)

FinalPathSA, FinalDistanceSA = SimulatedAnnealing(path = InitialPath.copy())

print('\n\n\n\n(SA)Final Path: ',FinalPathSA,'\n(SA)Final Distance: ',FinalDistanceSA, '\n\nDistances:\n',d)