import random
from random import shuffle
import copy
import math

from config import NB_BEES, BEEHIVE_POSITION


class Beehive:
    
    def __init__(self, flowers):
        self.flowers = flowers

    def __str__(self):
        return f"beehive has {len(self.flowers)} flowers."

    def init_bee(self)->list:
        path = copy.copy(self.flowers)
        shuffle(path)
        return path
    

    def init_bees(self)->list[tuple]:
        self.bees = []
        for b in range(NB_BEES):
            new_bee:list = self.init_bee()
            new_bee.insert(0,(BEEHIVE_POSITION))
            # Pour l'insertion de la ruche en fin de liste, pas besoin de "Insert", on garde "append"
            new_bee.append((BEEHIVE_POSITION))
            self.bees.append(new_bee)
        # print(self.bees)
        return self.bees

    # def  compute_segment(self, p1, p2):
    #     # print(p1, p2)
    #     dx = p1[0] - p2[0]
    #     dy = p1[1] - p2[1]
    #     length = (dx**2 + dy**2)**0.5
        # return length

        
    def compute_path(self, bee_path:list[list[tuple]])->list:
        dist_for_each_bee = []
        itertion = 0
        for bee in bee_path:
            distance = 0
            itertion += 1
            for i in range(len(bee)-1):
                # Utilisation de la fonction "math" pour calculer la distance euclidienne
                gap = math.dist(bee[i], bee[i+1])
                distance += gap
                
            dist_for_each_bee.append(distance)
            # print(distance)
            # print(f'Total distance for bee_{itertion} = {distance}')
        return dist_for_each_bee   
        
        # length = 0
        # for i in range(len(path)-1) :
        #     length += self.compute_segment(path[i], path[i+1])
        # return length

    def print_average_distance(self):
        l=0
        avrg_dist = 0
        l = self.compute_path(self.bees)
        for dist in l:
            avrg_dist = avrg_dist + dist
        avrg_dist = avrg_dist/(len(l))
       
        print(f"La distance moyenne est de {avrg_dist}")

class Gen_evo:

    # Tri par rang, on garde les 10 meilleures.
    # def selection(self, bees: list[tuple], list_of_dist: list) -> list[tuple]:
    #     n = len(list_of_dist)

    #     for i in range(n):
    #         for j in range(0, n - i - 1):
    #             if list_of_dist[j] > list_of_dist[j + 1]:
    #                 list_of_dist[j], list_of_dist[j + 1] = list_of_dist[j + 1], list_of_dist[j]
    #                 bees[j], bees[j + 1] = bees[j + 1], bees[j]

    #     print(list_of_dist[:10])
    #     return bees[:10]

    def selection (self, list_of_dist, bees, nb_survivants):
        pair = list(zip(list_of_dist, bees))
        pair.sort(key=lambda p: p[0])
        best_bees = [bee for dist, bee in pair[:nb_survivants]]
        return best_bees

    def crossover_pair(self, parent1, parent2):
        p1 = parent1[1:-1]
        p2 = parent2[1:-1]
        n = len(p1)
 
        a, b = sorted(random.sample (range(n),2))
        child = [None]*n
        child [a:b+1] = p1[a:b+1]

        choosen_flowers = set(child[a:b+1])
        left_spaces = [f for f in p2 if f not in choosen_flowers]
        it=iter(left_spaces)
        for i in range(n):
            if child[i] is None : 
                child[i] = next(it)

        child.insert(0, BEEHIVE_POSITION)
        child.append(BEEHIVE_POSITION)
        return child

    def crossover(self, best_bees, total_bees):
        new_generation = []
        while len(new_generation)<total_bees:
            parent1, parent2 = random.sample(best_bees, 2)
            child = self.crossover_pair(parent1, parent2)
            new_generation.append(child)
        return new_generation

    def mutations(self, new_generation, mutation_rate):
        for bee in new_generation :
            if random.random() < mutation_rate :
                n = len(bee)
                a, b = random.sample(range(1, n-1), 2)
                bee[a], bee[b] = bee[b], bee[a]
        return new_generation
