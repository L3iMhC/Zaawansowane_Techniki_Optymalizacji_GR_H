from docplex.mp.model import Model
import numpy as np
import generator as gen
n = 10
m = Model(name='test')

generator = gen.RandomNumberGenerator(578)

S=[]
for i in range(0, n):
        S.append(generator.nextInt(-100,100))
T = generator.nextInt(-50*n,50*n);

y = [ m.binary_var(name='y{0}'.format(i)) for i in range(0,n) ]

m.minimize(m.abs(T-m.sum(y[i]*S[i] for i in range(0,n))))

m.solve()
m.print_solution()
