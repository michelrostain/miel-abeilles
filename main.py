import pandas as pd
from beehive import Beehive, Evolution
from visualization import Visualization

def load_data(path):
    field = pd.read_csv(path)
    flower_field = list(zip(field["x"], field["y"]))
    return flower_field

def main():
    
    flower_field = load_data("champ_fleurs.csv")
    beehive = Beehive(flower_field) 
    beehive.build_graph()
    beehive.init_bees()
   
    evolution = Evolution(beehive)
   
    visualization = Visualization(beehive)
    queen_distances, mean_distances = evolution.evolution()
    visualization.plot_evolution(queen_distances, mean_distances)
    visualization.plot_best_path()
    visualization.plot_genealogy()

if __name__ == "__main__":
    main()    