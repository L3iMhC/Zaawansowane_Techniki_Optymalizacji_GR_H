import time
from docplex.mp.model import Model
import numpy as np
import generator as gen
from matplotlib import pyplot as plt

size = 40
solutions = np.zeros((size))

for n in range(1, size, 1):

    generator = gen.RandomNumberGenerator(654)

    m = Model(name='test{0}'.format(n))
    m.float_precision = 4
    S = []
    for i in range(0, n):
        S.append(generator.nextInt(-100, 100))
    T = generator.nextInt(-50*n, 50*n)

    y = [m.binary_var(name='y{0}'.format(i)) for i in range(0, n, 1)]

    m.minimize(m.abs(T-m.sum(y[i]*S[i] for i in range(0, n))))

    # m.print_solution()
    solutions[n] = m.solve().objective_value


x = np.arange(0, size)
print(solutions)
plt.title("Wynik minimalizacji w zależności od liczby zmiennych")
plt.xlabel("Liczba zmiennych")
plt.ylabel("Wynik minimalizacji")
plt.plot(x, solutions, "o")
plt.show()
