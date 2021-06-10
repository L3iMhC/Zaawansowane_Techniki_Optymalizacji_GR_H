# Kryteria 2, 3, 4, 5
# Wizualizacja 1, 3, 4, 7

import generator as gen
import numpy as np
import random
from matplotlib import pyplot as plt

Z = 4124
generator = gen.RandomNumberGenerator(Z)


def all_task_done_time(schedule, n, m, p, d, ktore_kryteria_zwrocic=[2, 3, 4, 5]):
    # C[zadanie][maszyna]
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

    F = 0
    T_max = 0
    T_sum = 0
    L_max = 0
    for i in range(0, n):
        # Suma czasow zakonczenia wszystkich zadan
        F += C[schedule[i]][2]
        # Maksymalne spóźnienie zadania
        T_max = max(T_max, max(C[schedule[i]][2] - d[j], 0))
        # Suma spóźnień zadań
        T_sum += max(C[schedule[i]][2] - d[j], 0)
        # Maksymalna nieterminowość zadania
        L_max = max(L_max, C[schedule[i]][2] - d[j])
    if(ktore_kryteria_zwrocic == [2, 3]):
        return [F, T_max]
    if(ktore_kryteria_zwrocic == [2, 3, 4]):
        return [F, T_max, T_sum]
    if(ktore_kryteria_zwrocic == [2, 3, 4, 5]):
        return [F, T_max, T_sum, L_max]
    return C[schedule[-1]][-1]

# SZABLON
# def do_zadanie1(min_tasks=4, max_tasks=10):
#     m = 3
#     for n in range(min_tasks, max_tasks+1):
#         A = 0
#         # Generacja instancji
#         p = np.zeros((n, m))
#         d = np.zeros((n))
#         initial_schedule = np.zeros(n, dtype=np.int32)
#         for i in range(0, n):
#             initial_schedule[i] = i
#             for j in range(0, m):
#                 p[i][j] = generator.nextInt(1, 99)
#                 A += p[i][j]
#         B = A//2
#         A = A//6
#         for i in range(0, n):
#             d[j] = generator.nextInt(A, B)
#         # Losowanie początkowego harmonogramu
#         # np.random.shuffle(initial_schedule)
#         print(all_task_done_time(
#             initial_schedule, n, m, p, d, [2, 3, 4, 5]))
#         print(p)
#         print(initial_schedule)

# Zadanie 1


def is_dominated(k_x_prim, k_x):
    betters = 0
    for i in range(len(k_x)):
        if k_x_prim[i] >= k_x[i]:
            return False
        if k_x_prim[i] < k_x[i]:
            betters += 1
    if(betters > 0):
        return True
    else:
        return False


def make_Pareto_from_P(P):
    F = P.copy()
    # Z jakiegos powodu jak sie to robi w petli to dziala lepiej xd - ale dalej nie idealnie
    for i in range(0, 10):
        for a in F:
            for b in F:
                if(a != b and is_dominated(b, a)):
                    F.remove(a)
                    break
    return F


# Sumujemy prostokaty
def calculate_HVI(F):
    z1 = 1.2*max(F[:, 0])
    z2 = 1.2*max(F[:, 1])
    HVI = 0

    # Posortowanie F malejaco w zaleznosci od F[:,0]
    for i in range(len(F)):
        if i == 0:
            x = z1-F[i, 0]
        else:
            x = F[i-1, 0] - F[i, 0]
        y = z2-F[i, 1]
        HVI += x*y

    return HVI


def do_zadanie1(min_tasks=4, max_tasks=10):
    m = 3
    for n in range(min_tasks, max_tasks+1):
        A = 0
        # Generacja instancji
        p = np.zeros((n, m))
        d = np.zeros((n))
        initial_schedule = np.zeros(n, dtype=np.int32)
        for i in range(0, n):
            initial_schedule[i] = i
            for j in range(0, m):
                p[i][j] = generator.nextInt(1, 99)
                A += p[i][j]
        B = A//2
        A = A//6
        for i in range(0, n):
            d[j] = generator.nextInt(A, B)

        max_iterations = 10
        for max_iterations in [100, 200, 400, 800, 1600]:
            P = []
            iters = 0
            random.shuffle(initial_schedule)
            x = initial_schedule
            P.append(all_task_done_time(x, n, m, p, d, [2, 3]))
            while iters < max_iterations:
                j = generator.nextInt(0, len(x)-1)
                i = generator.nextInt(0, len(x)-1)
                while j == i:
                    i = generator.nextInt(0, len(x)-1)
                x_prim = x.copy()
                x_prim[i], x_prim[j] = x_prim[j], x_prim[i]
                if(is_dominated(all_task_done_time(x_prim, n, m, p, d, [2, 3]), all_task_done_time(x, n, m, p, d, [2, 3])) or random.random() < pow(0.995, iters)):
                    P.append(all_task_done_time(x_prim, n, m, p, d, [2, 3]))
                x = x_prim
                iters += 1
            F = make_Pareto_from_P(P)
            print(F)
            F = np.array(F)
            P = np.array(P)
            #print(F[:, 0])
            #print(F[:, 1])
            # np.sort(F[:,0])
            # F[F[:,1].argsort()[::-1]]
            F = F[(-F[:, 0]).argsort()]
            print(F)
            plt.plot(P[:, 1], P[:, 0], 'bo')
            plt.plot(F[:, 1], F[:, 0], 'ro-')
            plt.show()

            HVI = calculate_HVI(F)
            print("\nHVI:", HVI, "\n###\n")
            worse = find_worse_result(F, P)
            results_range = find_range_of_results(F, worse)
            criterias_with_results = {
                "Pareto": F, "Worse": worse, "Range": results_range
            }

            prepared_data = prepare_data(F, worse)
            print(prepared_data)

            prepared_data = normalize_data(prepared_data, results_range)

            # Słupkowy
            barWidth = 0.25
            r1 = np.arange(len(prepared_data[0]))
            r2 = [x + barWidth for x in r1]

            plt.bar(r1, prepared_data[0], color='#7f6d5f',
                    width=barWidth, edgecolor='white', label='Kryterium 1')
            plt.bar(r2, prepared_data[1], color='#557f2d',
                    width=barWidth, edgecolor='white', label='Kryterium 2')
            plt.xlabel('Numer rozwiązania', fontweight='bold')
            plt.xticks([r + barWidth for r in range(len(prepared_data[0]))],
                       ['Rozw. 1', 'Rozw. 2', 'Rozw. 3', 'Rozw. 4'])
            plt.legend()
            plt.show()


def normalize_data(data, data_range):
    normalized_data = []
    for i in range(len(data)):
        normalzied_single_criteria_data = []
        for single_value in data[i]:
            norm_value = (
                single_value-data_range[i]["Min"])/(data_range[i]["Max"]-data_range[i]["Min"])
            normalzied_single_criteria_data.append(norm_value)
        normalized_data.append(normalzied_single_criteria_data)
    return normalized_data


def prepare_data(F, worse):
    criterias = []
    for i in range(len(worse)):
        single_criteria_results = []
        for f in F:
            if(len(single_criteria_results) > 2):
                break
            single_criteria_results.append(f[i])
        single_criteria_results.append(worse[i])
        criterias.append(single_criteria_results)
    return criterias


def find_range_of_results(F, worse):
    ranges = []
    for criteria_no in range(len(worse)):
        minValue = worse[criteria_no]
        maxValue = worse[criteria_no]
        for f in F:
            if minValue > f[criteria_no]:
                minValue = f[criteria_no]
            if maxValue < f[criteria_no]:
                maxValue = f[criteria_no]
        ranges.append({"Min": minValue, "Max": maxValue})
    return ranges


def find_worse_result(F, P):
    print(P, F)
    for p in P:
        for f in F:
            if p[0] > f[0] and p[1] > f[1]:
                return p
    return [999999999, 999999999]


def do_visualization(criterias_with_results):
    None


do_zadanie1(10, 10)
