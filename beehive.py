import random
from random import shuffle
import copy
import math
from config import NB_BEES, BEEHIVE_POSITION


class Bee:
    '''
    Une abeille : son chemin + son historique (pour l'arbre généalogique).
    '''
    # Compteur partagé par toutes les abeilles : chaque nouvelle abeille
    # reçoit un identifiant unique (0, 1, 2, ...)
    _next_id = 0

    def __init__(self, path, generation=0, parents=None):
        self.bee_id = Bee._next_id
        Bee._next_id += 1
        self.path = path              # liste de coordonnées, ruche au début et à la fin
        self.generation = generation  # 0 = population de départ
        self.parents = parents        # None, ou tuple (parent1, parent2) d'objets Bee


class Beehive:
    
    def __init__(self, flowers):
        self.flowers = flowers

    def __str__(self):
        return f"beehive has {len(self.flowers)} flowers."

    def init_bee(self)->list:
        path = copy.copy(self.flowers)
        shuffle(path)
        return path
    
    def init_bees(self)->list[Bee]:
        self.bees = []
        for b in range(NB_BEES):
            path:list = self.init_bee()
            path.insert(0,(BEEHIVE_POSITION))
            # Pour l'insertion de la ruche en fin de liste, pas besoin de "Insert", on garde "append"
            path.append((BEEHIVE_POSITION))
            # Abeille de la génération 0, sans parents
            self.bees.append(Bee(path))
        # print(self.bees)
        return self.bees

    def compute_path(self, bees:list[Bee])->list:
        dist_for_each_bee = []
        itertion = 0
        for bee in bees:
            distance = 0
            itertion += 12020
            path = bee.path  # le chemin est maintenant dans l'attribut "path" de l'abeille
            for i in range(len(path)-1):
                # Utilisation de la fonction "math" pour calculer la distance euclidienne
                gap = math.dist(path[i], path[i+1])
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

    def selection (self, list_of_dist, bees, nb_survivants):
        pair = list(zip(list_of_dist, bees))
        pair.sort(key=lambda p: p[0])
        best_bees = [bee for dist, bee in pair[:nb_survivants]]
        return best_bees

    def crossover_pair(self, parent1, parent2, generation):
        # [1:-1] retire la ruche du début et de la fin
        p1 = parent1.path[1:-1]
        p2 = parent2.path[1:-1]
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
        # L'enfant garde la trace de ses deux parents et de sa génération
        return Bee(child, generation=generation, parents=(parent1, parent2))

    def crossover(self, best_bees, total_bees, generation):
        new_generation = []
        while len(new_generation)<total_bees:
            parent1, parent2 = random.sample(best_bees, 2)
            child = self.crossover_pair(parent1, parent2, generation)
            new_generation.append(child)
        return new_generation

    def mutations(self, new_generation, mutation_rate):
        for bee in new_generation :
            if random.random() < mutation_rate :
                path = bee.path
                n = len(path)
                a, b = random.sample(range(1, n-1), 2)
                path[a], path[b] = path[b], path[a]
        return new_generation