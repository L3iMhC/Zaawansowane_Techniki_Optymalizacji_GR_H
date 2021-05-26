import generator as gen
import numpy as np
import random

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

            indexes=[]
            items1 = parent1[crossing_point1:crossing_point2]
            for item in items1:
                for i in range (0,len(parent2)):
                    if(parent2[i]==item):
                        indexes.append(i)
            indexes.sort()
            items2=[]

            child2 = parent2
            for index in indexes:
                items2.append(parent2[index])
                child2[index] = items1[indexes.index(index)]

            child1[:crossing_point1] = parent1[:crossing_point1]
            child1[crossing_point2:] = parent1[crossing_point2:]
            child1[crossing_point1:crossing_point2] = items2
            
            if np.array_equal(parent1, child1) & np.array_equal(parent2, child2):
                continue
            else:
                #print("\nChild Creation:\n", indexes)
                #print("Parent1: ", parent1, "\nParent2: ", parent2, "\nChild1: ", child1, "\nChild2: ", child2, "\n###############\n")
                if not np.array_equal(parent1, child1):
                    children.append(child1)
                if not np.array_equal(parent2, child2):
                    children.append(child2)
                    print("\n!!!!!!!!!!!!!!!!!!!!CHILD2CHANGED!!!!!!!!!!!!!!!!!!\n")
                    print("\nChild Creation:\n", indexes)
                    print("Parent1: ", parent1, "\nParent2: ", parent2, "\nChild1: ", child1, "\nChild2: ", child2, "\n###############\n")
    return children

# Mutacja do implementacji


def do_mutation(child):
    for i in range(0, len(child)):
        probability = random.uniform(0.0, 100.0)
        if(probability<=5):
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
    for i in range (0, len(whole_population)):
        results.append(all_task_done_time(whole_population[i], n, m, p))

    for i in range (0, len(population)):
        if (i < len(population)/10):
            index = results.index(min(results))
        else:
            index = random.randint(0,len(whole_population)-1)

        new_population.append(whole_population.pop(index))
        del results[index]

    #print("###################")
    #print("Population:     ", population)
    #print("Children:       ", children)
    #print("New_population: ", new_population)
    #print("###################")

    return new_population


def do_ga(initial_schedule, n, m, p, initial_population_size=5):
    # Najlepsza dotychczasowa wartość

    best_value = all_task_done_time(initial_schedule, n, m, p)
    best_schedule = initial_schedule
    # Zmiana na schedule dla lepszej czytelności
    schedule = initial_schedule
    # Bieżąca populacja
    population = []
    population.append(initial_schedule)
    # Generacja populacji początkowej
    for _ in range(0, initial_population_size):
        np.random.shuffle(schedule)
        population.append(np.copy(schedule))
        value = all_task_done_time(schedule, n, m, p)
        if value < best_value:
            best_value = value
            best_schedule = schedule
    iterations = 0
    while iterations != 1:
        parents = select_parents(population, 6)
        children = do_cross_over1(parents)
        for child in children:
            value = all_task_done_time(child, n, m, p)
            if value < best_value:
                best_value = value
                best_schedule = child
            mutationed_child = do_mutation(child)
            if not np.array_equal(child, mutationed_child):
                mutationed_value = all_task_done_time(
                    mutationed_child, n, m, p)
                if mutationed_value < best_value:
                    best_value = mutationed_value
                    best_schedule = mutationed_child
        population = make_new_population(population, children, n, m, p)

        iterations += 1
    return best_schedule, best_value


def do_experiments(repeats=1, min_tasks=5, max_tasks=5, min_machines=2, max_machines=3):
    for n in range(min_tasks, max_tasks+1):
        for m in range(min_machines, max_machines+1):
            random_shuffle_minimalization_values = []
            for _ in range(0, repeats):
                # Generacja instancji
                p = np.zeros((n, m))
                initial_schedule = np.zeros(n, dtype=np.int32)
                for i in range(0, n):
                    initial_schedule[i] = i
                    for j in range(0, m):
                        p[i][j] = generator.nextInt(1, 99)
                # Losowanie początkowego harmonogramu
                np.random.shuffle(initial_schedule)
                # Dodanie wartości czasu końcowego dla początkowego harmonogramu
                random_shuffle_minimalization_values.append(
                    all_task_done_time(initial_schedule, n, m, p))
                # Minimalizacja algorytmem genetycznym
                do_ga(initial_schedule, n, m, p)

            print("Random shuffle for", n, "tasks and", m, "machines", "mean minimalization value=", sum(
                random_shuffle_minimalization_values)//repeats)


do_experiments(repeats=1, max_tasks=20, max_machines=10)
