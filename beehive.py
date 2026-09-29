import matplotlib.pyplot as plt
import networkx as nx
import math
import random
from statistics import mean

from config import NB_BEES, MUTATION_RATE, TOURNAMENT_SIZE, NB_GENERATIONS, REPRODUCTION_RATE 

class Bee:
    next_id = 0

    def __init__(self, path, parents, generation):
        self.bee_id = Bee.next_id
        Bee.next_id += 1
        self.path = path
        self.parents = parents
        self.generation = generation

        

class Beehive:
    def __init__(self, flowers):
        self.flowers = flowers
        self.hive = (500,500)
        self.graph = nx.Graph()
        self.hive_node = len(self.flowers)
        self.queen = None
        
    
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
        path = list(range(len(self.flowers)))
        random.shuffle(path)
        bee = Bee(path, None, 0)
        
        return bee

    def init_bees(self):
        self.bees = []
        for i in range(NB_BEES):
            bee = self.init_bee()
            self.bees.append(bee)

    def distance(self, flower1, flower2):
        x1, y1 = flower1
        x2, y2 = flower2
        return math.sqrt((x2-x1)**2+(y2-y1)**2)


    def total_distance(self, bee):
        total = 0
        total += self.graph[self.hive_node][bee.path[0]]["weight"]

        for i in range(len(bee.path)- 1):
            total += self.graph[bee.path[i]][bee.path[i+1]]["weight"]
        total += self.graph[bee.path[-1]][self.hive_node]["weight"]

        return total    

    def plot_best_path(self):
        route = [self.hive_node] + self.queen.path + [self.hive_node]
        route_edges = []
        for i in range(len(route)-1):
            route_edges.append((route[i], route[i + 1])) 
        pos = nx.get_node_attributes(self.graph, "pos")  

        nx.draw_networkx_nodes(self.graph, pos, nodelist=range(len(self.flowers)), node_size=50)     
        nx.draw_networkx_edges(self.graph, pos, edgelist=route_edges, width=1 )
        nx.draw_networkx_nodes(self.graph, pos, nodelist=[self.hive_node], node_size=150)
        plt.title("Best bee path")
        plt.show()
     

    def plot_genealogy(self):
        genealogy = nx.DiGraph()
        visited = set()    
        
        def add_ancestors(bee):
            if bee.bee_id in visited:
                return

            visited.add(bee.bee_id)
            genealogy.add_node(bee.bee_id, generation=bee.generation)

            if bee.parents is not None:
                parent1, parent2 = bee.parents
                genealogy.add_edge(parent1.bee_id, bee.bee_id)
                genealogy.add_edge(parent2.bee_id, bee.bee_id)
                add_ancestors(parent1)
                add_ancestors(parent2)


        add_ancestors(self.queen)
        print("Genealogy bees:", genealogy.number_of_nodes())
        print("Genealogy relations:", genealogy.number_of_edges())
        
        
        pos = nx.multipartite_layout(genealogy, subset_key="generation")
             
        nx.draw(genealogy, pos, node_size=10, with_labels=False, arrows=True, connectionstyle="arc3,rad=0.15")
        plt.title("Genealogy of the best bee")
        plt.show()


class Evolution:
    def __init__(self, beehive):
        self.beehive = beehive    

    def selection(self):
        tournament = random.sample(self.beehive.bees, TOURNAMENT_SIZE)
        winner = min(tournament, key=self.beehive.total_distance)
        return winner


    def crossover(self, parent1, parent2, generation):
        cut1, cut2 = random.sample(range(len(parent1.path)), 2)

        if cut1 > cut2:
            cut1, cut2 = cut2, cut1

        child = [None] * len(parent1.path)    
        child[cut1:cut2] = parent1.path[cut1:cut2]

        for gene in parent2.path:
            if gene not in child:
                empty_position = child.index(None)
                child[empty_position] = gene

        new_bee = Bee(child, (parent1, parent2), generation)        

        return new_bee        

    def mutate(self, bee):
        if random.random() < MUTATION_RATE:
            index1, index2 = random.sample(range(len(bee.path)), 2)
            bee.path[index1], bee.path[index2] = bee.path[index2], bee.path[index1]
        return bee    

    
    def evolution(self):
        queen_distances = []
        mean_distances = []

        for generation in range(NB_GENERATIONS):
            distances = []

            for bee in self.beehive.bees:
                distance_value = self.beehive.total_distance(bee)
                distances.append(distance_value)

            min_distance = min(distances)
            mean_distance = mean(distances)
            queen_index = distances.index(min_distance)
            self.beehive.queen = self.beehive.bees[queen_index]
            queen_distances.append(min_distance)
            mean_distances.append(mean_distance)

            print("Generation", generation, "Queen distance:", min_distance)    

            sorted_bees = sorted(self.beehive.bees, key=self.beehive.total_distance)

            nb_replaced = int(REPRODUCTION_RATE * NB_BEES)

            best_bees = sorted_bees[:-nb_replaced]
            
            new_bees = []
            while len(new_bees)<nb_replaced:
                parent1 = self.selection()
                parent2 = self.selection()

                while parent2 == parent1:
                    parent2 = self.selection()

                child = self.crossover(parent1,parent2, generation + 1)    
                child = self.mutate(child)

                new_bees.append(child)
 
            self.beehive.bees = best_bees + new_bees 

        return queen_distances, mean_distances     

    def plot_evolution(self, queen_distances, mean_distances):

        plt.plot(range(1, len(queen_distances) + 1), queen_distances, label="Queen")
        plt.plot(range(1, len(mean_distances) + 1), mean_distances, label="Mean")
        
        plt.xlabel("Generation")
        plt.ylabel("Distance")
        plt.title("Evolution of distances")
        plt.show() 


   