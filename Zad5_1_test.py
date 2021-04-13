from docplex.mp.model import Model
import numpy as np
import generator as gen
import math

n=10

m = Model(name='test')

generator = gen.RandomNumberGenerator(578)

r = np.zeros(n, dtype=float)
a = np.zeros(n, dtype=float)
b = np.zeros(n, dtype=float)
for i in range(0, n):
        a[i] = generator.nextFloat(5,35)
        b[i] = generator.nextFloat(5,35)
        r[i] = generator.nextFloat(1,4)

x0 = generator.nextFloat(5,35)
y0 = generator.nextFloat(5,35)
p0 = [x0, y0]

point =[]
for i in range(0,n+2):
    point.append([m.continuous_var(name='point{0}{1}'.format(i,j)) for j in range(0,2)])

order = []
for i in range(0,n+2):
    order.append([m.integer_var(name='order{0}'.format(i))])


m.add_constraint(point[0][j] for j in range(0, 2) == p[j])
m.add_constraint(point[n+1][j] for j in range(0, 2) == p[j])
m.add_constraint(order[0] == 0)
m.add_constraint(order[n+1] == n+1)

for i in range(1, n+1):
    m.add_constraint(point[i-1][0]  <= a[i-1]+r[i-1])
    m.add_constraint(point[i-1][0]  >= a[i-1]-r[i-1])
    m.add_constraint((point[i-1][1]  == sqrt(r[i-1]*r[i-1]-a[i-1]*a[i-1]) + b[i-1]) or (point[i-1][1]  == -sqrt(r[i-1]*r[i-1]-a[i-1]*a[i-1]) + b[i-1]))

#for i in range(1, n+1):

m.minimize(m.sum(sqrt(pow((x[order[i]][0]-x[order[i+1]][0],2)+(x[order[i]][1]-x[order[i+1]][1])**2)) for i in range(0,n))

m.solve()
m.print_solution()