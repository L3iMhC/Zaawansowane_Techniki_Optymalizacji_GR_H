from docplex.mp.model import Model
import numpy as np
import generator as gen
import math

n=5

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

m.add_constraint(point[0][0] == x0)
m.add_constraint(point[0][1] == y0)
m.add_constraint(point[n+1][0] == x0)
m.add_constraint(point[n+1][1] == y0)

for i in range(1, n+1):
    m.add_constraint(point[i][0]  <= a[i-1]+r[i-1])
    m.add_constraint(point[i][0]  >= a[i-1]-r[i-1])
    m.add_constraint(point[i][1]  <= b[i-1]+r[i-1])
    m.add_constraint(point[i][1]  >= b[i-1]-r[i-1])
    #m.add_constraint(point[i][1]  <= math.sqrt(r[i-1]**2-(point[i][0]-a[i-1])**2)+b[i-1]))
    #m.add_constraint(point[i][1]  >= -1*math.sqrt(r[i-1]**2-(point[i][0]-a[i-1])**2)+b[i-1])
    #m.add_constraint(math.sqrt((point[i][0]-a[i-1])**2+(point[i][1]-b[i-1])**2) <= r[i-1])
    m.add_constraint(m.abs(point[i][0]-a[i-1])+m.abs(point[i][1]-b[i-1]) <= r[i-1])

#for i in range(1, n+1):

#m.minimize(m.sum(math.sqrt((point[i-1][0]-point[i][0])**2+(point[i-1][1]-point[i][1])**2)) for i in range(1,n))
m.minimize(m.sum(m.abs(point[i-1][0]-point[i][0]) + m.abs(point[i-1][1]-point[i][1])) for i in range(1,n+2))

m.solve()
m.print_solution()
