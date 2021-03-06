import generator as gen
import numpy as np
import random
from matplotlib import pyplot as plt

Z = 4124
generator = gen.RandomNumberGenerator(Z)


def all_task_done_time(schedule, n, m, p):
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


def select_parents(population, parents_count):
    parents = []
    for i in range(0, parents_count):
        parents.append(population[generator.nextInt(0, len(population)-1)])
    return parents


def do_cross_over(parents):
    crossing_point1 = len(parents[0])//3
    crossing_point2 = len(parents[0])//3*2
    children = []
    for parent1 in parents:
        for parent2 in parents:
            if np.array_equal(parent1, parent2):
                continue
            child1, child2 = np.zeros(len(parent1), dtype=np.int32), np.zeros(
                len(parent1), dtype=np.int32)
            child1[:crossing_point1] = parent1[:crossing_point1]
            child1[crossing_point2:] = parent1[crossing_point2:]
            child1[crossing_point1:crossing_point2] = parent2[crossing_point1:crossing_point2]
            child2[:crossing_point1] = parent2[:crossing_point1]
            child2[crossing_point2:] = parent2[crossing_point2:]
            child2[crossing_point1:crossing_point2] = parent1[crossing_point1:crossing_point2]
            children.append(child1)
            children.append(child2)
    return children


def do_cross_over1(parents):
    crossing_point1 = len(parents[0])//3-1
    crossing_point2 = len(parents[0])//3*2+1
    children = []
    for parent1 in parents:
        for parent2 in parents:
            if np.array_equal(parent1, parent2):
                continue
            child1, child2 = np.zeros(len(parent1), dtype=np.int32), np.zeros(
                len(parent1), dtype=np.int32)

            indexes = []
            items1 = parent1[crossing_point1:crossing_point2]

            for item in items1:
                for i in range(0, len(parent2)):
                    if(parent2[i] == item):
                        indexes.append(i)

            indexes.sort()
            items2 = []
            child2 = parent2.copy()

            for index in indexes:
                items2.append(parent2[index])
                #print("\nOcochodzi:\n", parent2, parent2[index], index, items2)
                if not child2[index] == items1[indexes.index(index)]:
                    child2[index] = items1[indexes.index(index)]

            #print("\nItems check:\n", indexes, items2)
            #print("\n jeszcze parent", parent2, indexes, items2)

            child1[:crossing_point1] = parent1[:crossing_point1]
            child1[crossing_point2:] = parent1[crossing_point2:]
            child1[crossing_point1:crossing_point2] = items2

            if np.array_equal(parent1, child1) & np.array_equal(parent2, child2):
                continue
            else:
                #print("\nChild Creation:\nIndexes: ", indexes,"\nItems1:", items1,"\nItems2", items2)
                # print("\nParent1: ", parent1, "\nParent2: ", parent2, "\nChild1: ", child1, "\nChild2: ", child2, "\n###############\n")
                if not np.array_equal(parent1, child1):
                    children.append(child1)
                if not np.array_equal(parent2, child2):  # To sie nigdy nie wywoluje
                    children.append(child2)
                    # print("\n!!!!!!!!!!!!!!!!!!!!CHILD2CHANGED!!!!!!!!!!!!!!!!!!\n")
                    #print("\nChild Creation:\n", indexes)
                    # print("Parent1: ", parent1, "\nParent2: ", parent2, "\nChild1: ", child1, "\nChild2: ", child2, "\n###############\n")
    return children

# Mutacja do implementacji


def do_mutation(child):
    for i in range(0, len(child)):
        probability = random.uniform(0.0, 100.0)
        if(probability <= 5//len(child)):
            index = random.randint(0, len(child)-1)
            while (i == index):
                index = random.randint(0, len(child)-1)
            #print("\nChild one:", child)
            child[i], child[index] = child[index], child[i]
            #print("\nChild po mutacji:", child)
    return child


def make_new_population(population, children, n, m, p):
    whole_population = population + children
    new_population = []
    results = []
    for i in range(0, len(whole_population)):
        results.append(all_task_done_time(whole_population[i], n, m, p))

    for i in range(0, len(population)):
        if (i < len(population)/10):
            index = results.index(min(results))
        else:
            index = random.randint(0, len(whole_population)-1)

        new_population.append(whole_population.pop(index))
        del results[index]

    # print("###################")
    #print("Population:     ", population)
    #print("Children:       ", children)
    #print("New_population: ", new_population)
    # print("###################")

    return new_population


def do_ga(initial_schedule, n, m, p, initial_population_size=10):
    # Najlepsza dotychczasowa warto????

    best_value = all_task_done_time(initial_schedule, n, m, p)
    best_schedule = initial_schedule
    # Zmiana na schedule dla lepszej czytelno??ci
    schedule = initial_schedule
    # Bie????ca populacja
    population = []
    population.append(initial_schedule)
    # Generacja populacji pocz??tkowej
    for _ in range(0, initial_population_size):
        np.random.shuffle(schedule)
        population.append(np.copy(schedule))
        value = all_task_done_time(schedule, n, m, p)
        if value < best_value:
            best_value = value
            best_schedule = schedule
            print("\nnew best value:", best_value)
    iterations = 0
    while iterations != 1:
        parents = select_parents(population, initial_population_size//2)
        children = do_cross_over1(parents)
        for child in children:
            value = all_task_done_time(child, n, m, p)
            if value < best_value:
                best_value = value
                best_schedule = child
                print("\nnew best value:", best_value)
                iterations = 0
            mutationed_child = do_mutation(child)
            if not np.array_equal(child, mutationed_child):
                mutationed_value = all_task_done_time(
                    mutationed_child, n, m, p)
                if mutationed_value < best_value:
                    best_value = mutationed_value
                    best_schedule = mutationed_child
                    print("\nnew best value:", best_value)
                    iterations = 0
        population = make_new_population(population, children, n, m, p)

        iterations += 1
    return best_schedule, best_value


def do_experiments(repeats=1, min_tasks=49, max_tasks=5, min_machines=2, max_machines=3, oneMachineCount=0):
    if oneMachineCount != 0:
        random_shuffle_values = []
        ga_values = []
        m = oneMachineCount
        for n in range(min_tasks, max_tasks+1):
            random_shuffle_minimalization_values = []
            ga_minimalization_values = []
            for _ in range(0, repeats):
                # Generacja instancji
                p = np.zeros((n, m))
                initial_schedule = np.zeros(n, dtype=np.int32)
                for i in range(0, n):
                    initial_schedule[i] = i
                    for j in range(0, m):
                        p[i][j] = generator.nextInt(1, 99)
                # Losowanie pocz??tkowego harmonogramu
                np.random.shuffle(initial_schedule)
                # Dodanie warto??ci czasu ko??cowego dla pocz??tkowego harmonogramu
                random_shuffle_minimalization_values.append(
                    all_task_done_time(initial_schedule, n, m, p))
                # Minimalizacja algorytmem genetycznym
                sc, value = do_ga(initial_schedule, n, m, p)
                ga_minimalization_values.append(value)
            rshuffle_mean = sum(
                random_shuffle_minimalization_values)//repeats
            ga_mean = sum(
                ga_minimalization_values)//repeats
            print("Random shuffle for", n, "tasks and", m, "machines",
                  "mean minimalization value=", rshuffle_mean)
            print("Genetic algorithm  for", n, "tasks and", m,
                  "machines", "mean minimalization value=", ga_mean)
            random_shuffle_values.append(rshuffle_mean)
            ga_values.append(ga_mean)
        x = np.arange(min_tasks, max_tasks+1)
        plt.title(
            "Warto???? minimalizacji permutacyjnego problemu przep??ywowego na jednej maszynie w zale??no??ci od wielko??ci instancji")
        plt.xlabel("Liczba zmiennych")
        plt.ylabel("Warto???? rozwi??zania")
        plt.plot(x, random_shuffle_values, "o", label="Random initial shuffle")
        plt.plot(x, ga_values, "o", label="Genetic algorithm")
        plt.legend()
        plt.show()
    else:
        for n in range(min_tasks, max_tasks+1):
            for m in range(min_machines, max_machines+1):
                random_shuffle_minimalization_values = []
                ga_minimalization_values = []
                for _ in range(0, repeats):
                    # Generacja instancji
                    p = np.zeros((n, m))
                    initial_schedule = np.zeros(n, dtype=np.int32)
                    for i in range(0, n):
                        initial_schedule[i] = i
                        for j in range(0, m):
                            p[i][j] = generator.nextInt(1, 99)
                    # Losowanie pocz??tkowego harmonogramu
                    np.random.shuffle(initial_schedule)
                    # Dodanie warto??ci czasu ko??cowego dla pocz??tkowego harmonogramu
                    random_shuffle_minimalization_values.append(
                        all_task_done_time(initial_schedule, n, m, p))
                    # Minimalizacja algorytmem genetycznym
                    sc, value = do_ga(initial_schedule, n, m, p)
                    ga_minimalization_values.append(value)
                rshuffle_mean = sum(
                    random_shuffle_minimalization_values)//repeats
                ga_mean = sum(
                    ga_minimalization_values)//repeats
                print("Random shuffle for", n, "tasks and", m, "machines",
                      "mean minimalization value=", rshuffle_mean)
                print("Genetic algorithm  for", n, "tasks and", m,
                      "machines", "mean minimalization value=", ga_mean)


do_experiments(repeats=1, max_tasks=50, max_machines=10, oneMachineCount=3)
