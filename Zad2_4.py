from docplex.mp.model import Model
import numpy as np
import generator as gen
n=10

m = Model(name='test')

generator = gen.RandomNumberGenerator(578)

w = np.zeros((n,n), dtype=int)
d = np.zeros((n,n), dtype=int)
for i in range(0, n):
    for j in range(0,n):
        w[i][j] = generator.nextInt(1,50)
        d[i][j] = generator.nextInt(1,50)


f = [ m.integer_var(ub = n-1, name='f{0}.format(i)') for i in range(0,n) ]

m.minimize(m.sum(w[i][j]*d[f[i]][f[j]] for i in range(0,n) for j in range(0,n)))


#m.add_constraint(m.sum(f[i]) == n)

m.solve()
m.print_solution()
