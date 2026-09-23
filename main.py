import csv
import pandas as pd
from beehive import Beehive,Gen_evo

def load_data(path:str)->list[tuple]:
    '''
    @parametre _
    '''
    print("Hello")
    flowers = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader) # Saute la ligne de titre
        for row in reader : 
            flowers.append((int(row[1]), int(row[2])))
    return(flowers)


def main():
    flowers = load_data("fleurs.csv")

    b = Beehive(flowers)
    bees = b.init_bees()
    list_dist = b.compute_path(bees)

    g = Gen_evo()
    g.selection(bees,list_dist)
    
    # print(flowers)
    # load_distance_dataframe(flowers)


if __name__=="__main__": # Permet d'exécuter le code uniquement si le fichier original est appelé (ici main.py) mais ne sera pas exécuté si importé dans un autre fichier.
    main()



