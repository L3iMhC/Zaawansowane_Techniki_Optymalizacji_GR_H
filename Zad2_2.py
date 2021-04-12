from docplex.mp.model import Model
import numpy as np
import generator as gen

n = 5
m = 10
generator = gen.RandomNumberGenerator(578)

K = min(n,m)
S=[]
D=[]
k = np.zeros((n,m), dtype=int)

for i in range(0,K):
    S.append(generator.nextInt(1,20))
    D.append(S[i])

if(n>m):
    for i in range(K,n):
        r = generator.nextInt(1,20)
        S.append(r)
        j = generator.nextInt(0,m-1)
        D[j] = D[j]+r
elif(n<m):
    for i in range(K,m):
        r = generator.nextInt(1,20)
        D.append(r)
        j = generator.nextInt(0,n-1)
        S[j] = S[j]+r
for i in range(0, n):
    for j in range(0,m):
        k[i][j] = generator.nextInt(1,30)

model = Model(name='test')

z = []
for i in range(0,n):
    z.append([model.integer_var(name='z{0}{1}'.format(i,j)) for j in range(0,m)])


model.minimize(model.sum(z[i][j]*k[i][j] for i in range(0,n) for j in range(0,m)))

for i in range(0, n):
    model.add_constraint(model.sum(z[i][j] for j in range(0, m)) == S[i])

for j in range(0, m):
    model.add_constraint(model.sum(z[i][j] for i in range(0, n)) == D[j])


model.solve()
model.print_solution()
