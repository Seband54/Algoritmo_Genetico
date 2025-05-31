# train_model.py
import random

# Grafo simple
GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'F'],
    'C': ['A', 'D', 'E', 'H'], 
    'D': ['B', 'C', 'E', 'F'],  
    'E': ['C', 'D', 'G'],
    'F': ['B', 'D', 'G'],
    'G': ['E', 'F', 'H'],
    'H': ['G', 'C']
}

DISTANCES = {
    ('A', 'B'): 5,
    ('A', 'C'): 6,
    ('B', 'D'): 4,
    ('B', 'F'): 8,
    ('C', 'D'): 7,
    ('C', 'E'): 4,
    ('C', 'H'): 10,
    ('D', 'E'): 3.5,
    ('D', 'F'): 5,
    ('E', 'G'): 2.5,
    ('F', 'G'): 10,
    ('G', 'H'): 5
}

# Aseguramos que también funcione en ambas direcciones
for (a, b), d in list(DISTANCES.items()):
    DISTANCES[(b, a)] = d

def generate_individual(start, end, blocked):
    path = [start]
    current = start
    visited = set([start] + blocked)
    while current != end:
        neighbors = [n for n in GRAPH.get(current, []) if n not in visited and n not in blocked]
        if not neighbors:
            break
        current = random.choice(neighbors)
        path.append(current)
        visited.add(current)
    return path

def fitness(individual, end, blocked):
    if any(n in blocked for n in individual):
        return float('inf')
    if individual[-1] != end:
        return float('inf')

    total_distance = 0
    for i in range(len(individual) - 1):
        edge = (individual[i], individual[i + 1])
        total_distance += DISTANCES.get(edge, float('inf'))
    return total_distance

def crossover(parent1, parent2):
    cut = min(len(parent1), len(parent2)) // 2
    child = parent1[:cut] + [n for n in parent2 if n not in parent1[:cut]]
    return child

def mutate(individual, blocked):
    if len(individual) < 2:
        return individual
    i = random.randint(0, len(individual) - 2)
    try:
        options = [n for n in GRAPH[individual[i]] if n not in individual and n not in blocked]
        if options:
            individual[i+1] = random.choice(options)
    except:
        pass
    return individual

def genetic_algorithm(start, end, blocked, generations=100, population_size=30):
    population = [generate_individual(start, end, blocked) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=lambda ind: fitness(ind, end, blocked))
        next_gen = population[:5]

        while len(next_gen) < population_size:
            p1, p2 = random.sample(population[:10], 2)
            child = crossover(p1, p2)
            if random.random() < 0.3:
                child = mutate(child, blocked)
            next_gen.append(child)

        population = next_gen

    best = min(population, key=lambda ind: fitness(ind, end, blocked))
    return best

