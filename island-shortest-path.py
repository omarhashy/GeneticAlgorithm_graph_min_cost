import random
import time


def generate_graph(n: int):
    graph = dict()

    for i in range(1, n + 1):
        if i not in graph:
            graph[i] = dict()
        graph[i][i] = 0
        for u in range(i + 1, n + 1):
            if u not in graph:
                graph[u] = dict()

            weight = random.randint(1, 1000)
            graph[i][u] = weight
            graph[u][i] = weight
    return graph


def print_graph(graph: dict) -> None:
    print("_" * 200)
    print("Island\t" + "| Ticket costs")
    for i in graph:
        print(f"{i}\t|", end=" ")
        for neighbor in graph[i]:
            print(f"island: {neighbor} cost: {graph[i][neighbor]} |", end=" ")
        print()
    print("_" * 200)


GRAPH_SIZE = 8
TARGET_LENGTH = 4
POPULATION_SIZE = 10
GEN_SET = [i for i in range(1, GRAPH_SIZE + 1)]
TESTS = 10
GRAPH = generate_graph(GRAPH_SIZE)


def get_parent(target_length: int):
    genes = random.sample(GEN_SET, TARGET_LENGTH)
    return genes


def initialize_population(population_size: int, target_length: int):
    population = []
    for _ in range(population_size):
        population.append(get_parent(target_length))
    return population


def get_fitness(individual: list):
    score = 0
    for i in range(1, len(individual)):
        node1, node2 = individual[i - 1], individual[i]
        score += GRAPH[node1][node2]
    return score


# uniform_crossover
def crossover(parent1: list, parent2: list):
    child1 = parent1.copy()
    child2 = parent2.copy()

    random.shuffle(child1)
    random.shuffle(child2)

    vis1 = set(child1)
    vis2 = set(child2)

    max_cross_nodes = len(parent1) // 2

    for i in range(len(parent1)):
        if max_cross_nodes == 0:
            break

        for u in range(len(parent2)):
            if child1[i] not in vis2 and child2[u] not in vis1:
                max_cross_nodes -= 1
                vis1.add(child2[u])
                vis2.add(child1[i])
                child1[i], child2[u] = child2[u], child1[i]
                break

    return child1, child2


def mutate(individual: list):
    index = random.randint(0, len(individual) - 1)
    child = individual.copy()
    child[index] = random.choice(list(set(GEN_SET).difference(set(child))))
    return child


maxF = 10000000000000
freq = dict()


def find_best_path(test):
    global maxF
    population = initialize_population(POPULATION_SIZE, TARGET_LENGTH)
    population.sort(key=get_fitness)
    best_indevidual = population[0]

    print(
        f"Generation {0}: Best Individual - {best_indevidual}, Fitness - {get_fitness(best_indevidual)}"
    )
    for generation in range(1, 100000):
        first_best_best_indevidual, second_best_best_indevidual = (
            population[0],
            population[1],
        )

        child1, child2 = crossover(
            first_best_best_indevidual, second_best_best_indevidual
        )
        child1, child2 = mutate(child1), mutate(child2)

        population.append(child1)
        population.append(child2)

        population.sort(key=get_fitness)

        if get_fitness(population[0]) < get_fitness(best_indevidual):
            best_indevidual = population[0]
            print(
                f"Generation {generation}: Best Individual - {best_indevidual}, Fitness - {get_fitness(best_indevidual)}"
            )

        population.pop()
        population.pop()

    print(
        f"Test {test + 1}: Best Individual - {best_indevidual}, Fitness -  {get_fitness(best_indevidual)}"
    )
    maxF = min(maxF, get_fitness(best_indevidual))
    if get_fitness(best_indevidual) not in freq:
        freq[get_fitness(best_indevidual)] = set()

    freq[get_fitness(best_indevidual)].add(tuple(best_indevidual))
    print("_" * 200)


def main():
    print_graph(GRAPH)
    start_time = time.time()
    for _ in range(TESTS):
        find_best_path(_)
    end_time = time.time()
    duration = end_time - start_time
    print("Time taken:", round(duration, 2), "seconds")
    print("Best Individual Cost For All tests:", maxF)
    for i in freq[maxF]:
        print("path :", i )


if __name__ == "__main__":
    main()
