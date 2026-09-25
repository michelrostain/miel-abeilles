import csv
from config import FLOWERS_PATH, NB_GENERATIONS, NB_SURVIVANT

from beehive import Gen_evo
from beehive import Beehive

def load_data(path:str)->list[tuple]:
    '''
    @parametre _
    '''
    flowers = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader) # Saute la ligne de titre
        for row in reader : 
            flowers.append((int(row[1]), int(row[2])))
    return(flowers)


def main():
    flowers = load_data(FLOWERS_PATH)

    b = Beehive(flowers)
    bees = b.init_bees()

    for i in range(NB_GENERATIONS):
        # b.next_generation()
        # print(f"Génération n°{i+1}")
        b.print_average_distance()

    # --- Test de la sélection (à déplacer plus tard dans next_generation) ---
    g = Gen_evo()
    list_of_dist = b.compute_path(bees)                        # distance de chaque abeille
    survivors = g.selection(list_of_dist, bees, NB_SURVIVANT)
    # print(survivors)  # les meilleures
    print(f"{len(survivors)} survivantes sélectionnées")    


if __name__=="__main__": # Permet d'exécuter le code uniquement si le fichier original est appelé (ici main.py) mais ne sera pas exécuté si importé dans un autre fichier.
    main()



