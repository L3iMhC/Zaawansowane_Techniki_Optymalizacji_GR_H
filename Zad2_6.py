from docplex.mp.model import Model
import numpy as np
import generator as gen
n=10

m = Model(name='test')
generator = gen.RandomNumberGenerator(578)

d = np.zeros((n,n), dtype=int)
for i in range(0, n):
    for j in range(0,n):
        d[i][j] = generator.nextInt(1,30)

m.solve()
m.print_solution()