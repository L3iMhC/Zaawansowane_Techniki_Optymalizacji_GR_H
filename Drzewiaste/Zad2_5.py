from ..CPLEX import generator as gen
import numpy as np

moduleName = '../CPLEX/generator'

n = 5
Z = 586
generator = gen.RandomNumberGenerator(Z)

C = np.zeros(n)
W = np.zeros(n)
B = generator.nextInt(5*n, 10*n)
for i in range(0, 5):
    C[i] = generator.nextInt(1, 30)
    W[i] = generator.nextInt(1, 30)
