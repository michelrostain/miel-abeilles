from random import shuffle
import copy
import math

from config import NB_BEES


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
            new_bee.insert(0,(500,500))
            # Pour l'insertion de la ruche en fin de liste, pas besoin de "Insert", on garde "append"
            new_bee.append((500,500))
            self.bees.append(new_bee)
        # print(self.bees)
        return self.bees

    
    def compute_path(self, bee_path:list[list[tuple]]):

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
            print(f'Total distance for bee_{itertion} = {distance}')
        return dist_for_each_bee   

        
# class Gen_evo:

#     # Tri par rang, on garde les 10 meilleures.
#     # def selection(self, bees: list[tuple], list_of_dist: list) -> list[tuple]:
#     #     n = len(list_of_dist)

#     #     for i in range(n):
#     #         for j in range(0, n - i - 1):
#     #             if list_of_dist[j] > list_of_dist[j + 1]:
#     #                 list_of_dist[j], list_of_dist[j + 1] = list_of_dist[j + 1], list_of_dist[j]
#     #                 bees[j], bees[j + 1] = bees[j + 1], bees[j]

#     #     print(list_of_dist[:10])
#     #     return bees[:10]

#     def selection (self, list_of_dist, bees, nb_survivants):
#         pair = list(zip(list_of_dist, bees))
#         pair.sort(key=lambda p: p[0])
#         return [bee for dist, bee in pair[:nb_survivants]]

#     def crossover(self):
#         pass

#     def mutations(self):
#         pass

