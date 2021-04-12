from docplex.mp.model import Model
import numpy as np
import generator as gen
n=10

m = Model(name='test')

generator = gen.RandomNumberGenerator(578)

k = np.zeros((n,n), dtype=int)

for i in range(0, n):
    for j in range(0,n):
        k[i][j] = generator.nextInt(1,50)

g=[]
for i in range(0,n):
    g.append([m.binary_var(name='g{0}{1}'.format(i,j)) for j in range(0,n)])


m.minimize(m.sum(g[i][j]*k[i][j] for i in range(0,n) for j in range(0,n)))

for i in range(0, n):
    m.add_constraint(m.sum(g[i][j] for j in range(0, n)) == 1)

for j in range(0, n):
    m.add_constraint(m.sum(g[i][j] for i in range(0, n)) == 1)

m.solve()
m.print_solution()
