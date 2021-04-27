
from docplex.mp.model import Model
n = 6
k = 4
m = Model(name='test')
#x = m.continuous_var(lb=-99, ub=199, name='x')
#x = [ m.integer_var(name='x1'),  m.integer_var(name='x2')]
#x = [ m.integer_var(name='x{0}.format(i)') for i in range(0,2) ]
x =[]
for i in range(0,n):
    x.append([m.binary_var(name='x{0}{1}'.format(i,j)) for j in range(0,k)])
#x = {(i,j): m.binary_var(name='x{0}{1}'.format(i,j))
#     for i in range(1, n + 1 )
#         for j in range(1, k+1)}
values = [
    [7,2,9,3],
    [0,6,7,1],
    [4,1,6,3],
    [1,4,8,5],
    [3,3,9,8],
    [3,2,2,2]
    ];
m.maximize(m.sum(x[i][j]*values[i][j] for i in range(0,n) for j in range(0,k)))

#m.maximize(m.sum(x[i,j]*values[i-1][j-1]
#                 for i in range(1, n + 1 ) for j in range(1, k+1)))

for i in range(0, n):
    m.add_constraint(m.sum(x[i][j] for j in range(0, k)) <= 1)

#for i in range(1, n + 1):
#    m.add_constraint(m.sum(x[i,j] for j in range(1, k+1)) <= 1)
m.solve()
m.print_solution()