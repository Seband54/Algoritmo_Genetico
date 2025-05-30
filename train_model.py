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

def generate_individual(start, end, blocked):
    path = [start]
    current = start
    visited = set([start] + blocked)
    while current != end:
        neighbors = [n for n in GRAPH[current] if n not in visited]
        if not neighbors:
            break
        current = random.choice(neighbors)
        path.append(current)
        visited.add(current)
    return path

def fitness(individual, end):
    if individual[-1] != end:
        return float('inf')
    return len(individual)

def crossover(parent1, parent2):
    cut = min(len(parent1), len(parent2)) // 2
    child = parent1[:cut] + [n for n in parent2 if n not in parent1[:cut]]
    return child

def mutate(individual):
    if len(individual) < 2:
        return individual
    i = random.randint(0, len(individual) - 2)
    try:
        new = random.choice(GRAPH[individual[i]])
        if new not in individual:
            individual[i+1] = new
    except:
        pass
    return individual

def genetic_algorithm(start, end, blocked, generations=100, population_size=30):
    population = [generate_individual(start, end, blocked) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=lambda ind: fitness(ind, end))
        next_gen = population[:5]

        while len(next_gen) < population_size:
            p1, p2 = random.sample(population[:10], 2)
            child = crossover(p1, p2)
            if random.random() < 0.3:
                child = mutate(child)
            next_gen.append(child)

        population = next_gen

    best = min(population, key=lambda ind: fitness(ind, end))
    return best
