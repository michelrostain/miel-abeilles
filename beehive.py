import matplotlib.pyplot as plt
import networkx as nx
import math
import random

from config import NB_BEES, MUTATION_RATE, TOURNAMENT_SIZE, NB_GENERATIONS, REPRODUCTION_RATE 

class Beehive:
    def __init__(self, flowers):
        self.flowers = flowers
        self.hive = (500,500)
        self.graph = nx.Graph()
        self.hive_node = len(self.flowers)
        self.queen = None
    

    def distance(self, flower1, flower2):
        x1, y1 = flower1
        x2, y2 = flower2
        return math.sqrt((x2-x1)**2+(y2-y1)**2)

    def build_graph(self):
        for i, coordinates in enumerate(self.flowers):
          self.graph.add_node(i, pos=coordinates)

        for i in range(len(self.flowers)):
           for j in range(i + 1, len(self.flowers)):
               weight = self.distance(self.flowers[i], self.flowers[j])
               self.graph.add_edge(i, j, weight=weight)  

        self.graph.add_node(self.hive_node, pos=self.hive)

        for i in range(len(self.flowers)):
            weight = self.distance(self.hive, self.flowers[i])
            self.graph.add_edge(i, self.hive_node, weight=weight)

    def init_bee(self):
        bee = list(range(len(self.flowers)))
        random.shuffle(bee)
        return bee

    def init_bees(self):
        self.bees = []
        for i in range(NB_BEES):
            bee = self.init_bee()
            self.bees.append(bee)


    def total_distance(self, bee):
        total = 0
        total += self.graph[self.hive_node][bee[0]]["weight"]

        for i in range(len(bee)- 1):
            total += self.graph[bee[i]][bee[i+1]]["weight"]
        total += self.graph[bee[-1]][self.hive_node]["weight"]

        return total    


    def selection(self):
        tournament = random.sample(self.bees, TOURNAMENT_SIZE)
        winner = min(tournament, key=self.total_distance)
        return winner




    def crossover(self, parent1, parent2):
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

    def mutate(self, bee):
        if random.random() < MUTATION_RATE:
            index1, index2 = random.sample(range(len(bee)), 2)
            bee[index1], bee[index2] = bee[index2], bee[index1]
        return bee    

    
    def evolution(self):
        queen_distances = []

        for generation in range(NB_GENERATIONS):
            distances = []

            for bee in self.bees:
                distance_value = self.total_distance(bee)
                distances.append(distance_value)

            min_distance = min(distances)
            queen_index = distances.index(min_distance)
            self.queen = self.bees[queen_index]
            queen_distances.append(min_distance)

            print("Generation", generation+1, "Queen distance:", min_distance)    

            sorted_bees = sorted(self.bees, key=self.total_distance)

            nb_replaced = int(REPRODUCTION_RATE * NB_BEES)

            best_bees = sorted_bees[:-nb_replaced]
            
            new_bees = []
            while len(new_bees)<nb_replaced:
                parent1 = self.selection()
                parent2 = self.selection()

                while parent2 == parent1:
                    parent2 = self.selection()

                child = self.crossover(parent1,parent2)    
                child = self.mutate(child)

                new_bees.append(child)

            self.bees = best_bees + new_bees 

        return queen_distances     

    def plot_evolution(self, queen_distances):
        plt.plot(range(1, len(queen_distances) + 1), queen_distances)
        plt.xlabel("Generation")
        plt.ylabel("Queen distance")
        plt.title("Evolution of the queen distance")
        plt.show() 