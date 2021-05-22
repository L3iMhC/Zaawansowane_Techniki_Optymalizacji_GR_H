import generator as gen
import numpy as np

n = 2
m = 3
Z = 4124
generator = gen.RandomNumberGenerator(Z)

p = np.zeros((n, m))
initial_schedule = np.zeros(n, dtype=np.int32)

for i in range(0, n):
    initial_schedule[i] = i
    for j in range(0, m):
        p[i][j] = generator.nextInt(1, 99)

print(p)
np.random.shuffle(initial_schedule)
print(initial_schedule)


def all_task_done_time(schedule):
    C = np.zeros((n, m))
    for i in range(0, n):
        for j in range(0, m):
            if i == 0 and j == 0:
                C[schedule[i]][j] = p[schedule[i]][j]
            elif i > 0 and j == 0:
                C[schedule[i]][j] = C[schedule[i-1]][j] + p[schedule[i]][j]
            elif i == 0 and j > 0:
                C[schedule[i]][j] = C[schedule[i]][j-1] + p[schedule[i]][j]
            else:
                C[schedule[i]][j] = max(
                    C[schedule[i]][j-1], C[schedule[i-1]][j]) + p[schedule[i]][j]
    return C[schedule[-1]][-1]


print(all_task_done_time(initial_schedule))
