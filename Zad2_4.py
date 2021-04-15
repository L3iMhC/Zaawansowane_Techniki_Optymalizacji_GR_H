from docplex.mp.model import Model
import numpy as np
import generator as gen
n = 30

m = Model(name='test')

generator = gen.RandomNumberGenerator(578)

w = np.zeros((n, n), dtype=int)
d = np.zeros((n, n), dtype=int)
for i in range(0, n):
    for j in range(0, n):
        w[i][j] = generator.nextInt(1, 50)
        d[i][j] = generator.nextInt(1, 50)


f = {(i, j): m.binary_var(name='f[{0},{1}]'.format(i, j))
     for i in range(1, n+1) for j in range(1, n+1)}

for i in range(1, n+1):
    m.add_constraint(m.sum(f[i, j] for j in range(1, n+1)) == 1)
    m.add_constraint(m.sum(f[j, i] for j in range(1, n+1)) == 1)

m.minimize(m.sum(w[i-1][j-1]*d[i-1][j-1]*f[i, j]
           for i in range(1, n+1) for j in range(1, n+1)))


#m.add_constraint(m.sum(f[i]) == n)

m.solve()
m.print_solution()
