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

# Valores arbitrarios de velocidad (cuanto mayor, más rápido)
SPEED = {
    ('A', 'B'): 1.0,
    ('A', 'C'): 1.2,
    ('B', 'D'): 1.0,
    ('B', 'F'): 0.6,
    ('C', 'D'): 0.8,
    ('C', 'E'): 1.5,
    ('C', 'H'): 0.7,
    ('D', 'E'): 1.0,
    ('D', 'F'): 0.9,
    ('E', 'G'): 1.3,
    ('F', 'G'): 0.5,
    ('G', 'H'): 1.2
}

# Simétrico
for (a, b), v in list(SPEED.items()):
    SPEED[(b, a)] = v

SECURITY = {
    ('A', 'B'): 0.9,  # 1 = muy seguro, 0 = muy peligroso
    ('A', 'C'): 0.95,   
    ('B', 'D'): 0.6,
    ('B', 'F'): 0.3,
    ('C', 'D'): 0.8,
    ('C', 'E'): 0.7,
    ('C', 'H'): 0.4,
    ('D', 'E'): 0.85,
    ('D', 'F'): 0.5,
    ('E', 'G'): 0.9,
    ('F', 'G'): 0.2,
    ('G', 'H'): 0.95
}

for (a, b), s in list(SECURITY.items()):
    SECURITY[(b, a)] = s

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

def fitness(individual, end, blocked, alpha=0.5, beta=0.3, gamma=0.2):
    """
    alpha = peso de la distancia
    beta = peso del tiempo estimado (distancia / velocidad)
    gamma = penalización por inseguridad (1 - seguridad)
    """

    if any(n in blocked for n in individual):
        return float('inf')
    if individual[-1] != end:
        return float('inf')

    distance = 0
    time = 0
    risk = 0

    for i in range(len(individual) - 1):
        a, b = individual[i], individual[i + 1]
        d = DISTANCES.get((a, b), float('inf'))
        v = SPEED.get((a, b), 0.1)  # evitar división por cero
        s = SECURITY.get((a, b), 0.5)

        distance += d
        time += d / v
        risk += (1 - s) * d  # peso del riesgo según distancia expuesta

    score = alpha * distance + beta * time + gamma * risk
    return score

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

def genetic_algorithm(start, end, blocked, generations=100, population_size=30, alpha=0.5, beta=0.3, gamma=0.2):
    population = [generate_individual(start, end, blocked) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=lambda ind: fitness(ind, end, blocked, alpha, beta, gamma))
        next_gen = population[:5]

        while len(next_gen) < population_size:
            p1, p2 = random.sample(population[:10], 2)
            child = crossover(p1, p2)
            if random.random() < 0.3:
                child = mutate(child, blocked)
            next_gen.append(child)

        population = next_gen

    best = min(population, key=lambda ind: fitness(ind, end, blocked, alpha, beta, gamma))
    return best, evaluate_path(best)

def evaluate_path(individual):
    distance = 0
    time = 0
    risk = 0

    for i in range(len(individual) - 1):
        a, b = individual[i], individual[i + 1]
        d = DISTANCES.get((a, b), float('inf'))
        v = SPEED.get((a, b), 0.1)
        s = SECURITY.get((a, b), 0.5)

        distance += d
        time += d / v
        risk += (1 - s) * d

    return {
        "distance": round(distance, 2),
        "time": round(time, 2),
        "risk": round(risk, 2)
    }
