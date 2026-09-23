import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import math
import random


field = pd.read_csv("champ_fleurs.csv")
flower_field = list(zip(field["x"], field["y"]))

def distance(flower1, flower2):
    x1, y1 = flower1
    x2, y2 = flower2

    return math.sqrt((x2-x1)**2+(y2-y1)**2)

G = nx.Graph()
for i, coordinates in enumerate(flower_field):
    G.add_node(i, pos=coordinates)     
  

for i in range(len(flower_field)):
    for j in range(i + 1, len(flower_field)):
        flower_field[i]
        flower_field[j]

        weight = distance(flower_field[i], flower_field[j])
        G.add_edge(i, j, weight=weight)

hive = (500,500)
hive_node = len(flower_field)

G.add_node(hive_node, pos=hive)

for i in range(len(flower_field)):
    weight = distance(hive, flower_field[i])
    G.add_edge(i, hive_node, weight=weight)




population = []

for i in range(100):
    chromosome = list(range(len(flower_field)))
    random.shuffle(chromosome)
    population.append(chromosome)


def total_distance(chromosome):
    total = 0
    total += G[hive_node][chromosome[0]]["weight"]

    for i in range(len(chromosome)- 1):
        total += G[chromosome[i]][chromosome[i+1]]["weight"]

    total += G[chromosome[-1]][hive_node]["weight"]

    return total    


def selection(population):
    tournament = random.sample(population, 3)
    winner = min(tournament, key=total_distance)
    return winner

parent1 = selection(population)
parent2 = selection(population)

while parent2 == parent1:
    parent2 = selection(population)


def crossover(parent1, parent2):
    cut1, cut2 = random.sample(range(len(parent1)), 2)

    if cut1 > cut2:
        cut1, cut2 = cut2, cut1

    child = [None] * len(parent1)    
    child[cut1:cut2] = parent1[cut1:cut2]

    for gene in parent2:
        if gene not in child:
            empty_position = child.index(None)
            child[empty_position] = gene

    return child        

def mutate(chromosome, mutation_rate=0.1):
    if random.random() < mutation_rate:
        index1, index2 = random.sample(range(len(chromosome)), 2)
        chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
    return chromosome    

  

queen_distances = []



for generation in range(100):

    distances = []
    for chromosome in population:
        distance_value = total_distance(chromosome)
        distances.append(distance_value)

    min_distance = min(distances)
    queen_index = distances.index(min_distance)
    queen = population[queen_index]

    queen_distances.append(min_distance)

    print("Generation", generation+1, "Queen distance:", min_distance)    

    new_population = [queen]
    while len(new_population)<100:
       parent1 = selection(population)
       parent2 = selection(population)

       while parent2 == parent1:
          parent2 = selection(population)

       child = crossover(parent1,parent2)    
       child = mutate(child)

       new_population.append(child)

    population = new_population  

plt.plot(range(1, 101), queen_distances)
plt.xlabel("Generation")
plt.ylabel("Queen distance")
plt.title("Evolution of the queen distance")
plt.show()    