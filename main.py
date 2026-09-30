import csv
from config import FLOWERS_PATH, NB_GENERATIONS, NB_SURVIVORS, NB_BEES, MUTATION_RATE

from beehive import Gen_evo
from beehive import Beehive
from visualization import Visualization


def load_data(path: str) -> list[tuple]:
    '''
    Lit le fichier CSV et renvoie la liste des coordonnées (x, y) des fleurs.
    '''
    flowers = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Saute la ligne de titre
        for row in reader:
            flowers.append((int(row[1]), int(row[2])))
    return flowers


def main(comments=True, every=100):
    '''
    Lance la simulation complète.
    Renvoie (b, best_distance, avg_history, best_history) :
    - b : la ruche, avec b.queen = la meilleure abeille de la dernière génération
    - best_distance : distance de cette meilleure abeille
    - avg_history / best_history : distance moyenne / meilleure distance par génération
    '''
    # verbose : affiche les résultats dans le terminal
    # every   : une ligne de progression toutes les 'every' générations
    flowers = load_data(FLOWERS_PATH)

    b = Beehive(flowers)
    bees = b.init_bees()  # population de départ : chemins aléatoires
    g = Gen_evo()

    avg_history = []   # distance moyenne de chaque génération
    best_history = []  # meilleure distance de chaque génération

    for i in range(NB_GENERATIONS):
        # 1. Évaluation : distance parcourue par chaque abeille
        list_of_dist = b.compute_path(bees)
        avg_history.append(sum(list_of_dist) / len(list_of_dist))
        best_history.append(min(list_of_dist))

        # 2. Sélection : on garde les meilleures (distances les plus courtes)
        best_bees = g.selection(list_of_dist, bees, NB_SURVIVORS)

        # 3. Reproduction : on complète la population avec des enfants
        nb_children = NB_BEES - len(best_bees)
        # i + 1 : numéro de génération des enfants (0 = population de départ)
        new_generation = g.crossover(best_bees, nb_children, i + 1)

        # 4. Mutation : petite chance de modifier le chemin d'un enfant
        new_generation = g.mutations(new_generation, MUTATION_RATE)

        # Nouvelle génération = survivants + enfants
        bees = best_bees + new_generation

        # (i+1) % every == 0 : vrai seulement aux générations 100, 200, 300...
        if comments and (i + 1) % every == 0:
            print(f"Génération {i+1} : distance moyenne = {avg_history[-1]:.1f}")

    # Résultat final : la meilleure abeille de la dernière génération
    final_dist = b.compute_path(bees)
    best_distance = min(final_dist)
    best_bee = bees[final_dist.index(best_distance)]
    b.queen = best_bee  # la visualisation va chercher la meilleure abeille ici

    if comments:
        gain = (1 - avg_history[-1] / avg_history[0]) * 100  # baisse de la moyenne en %
        print("--- Résultats ---")
        print(f"Distance moyenne : {avg_history[0]:.1f} (gén. 1) -> {avg_history[-1]:.1f} (gén. {NB_GENERATIONS}), soit -{gain:.1f} %")
        print(f"Meilleure distance finale : {best_distance:.1f}")
        print(f"Trajet de la meilleure abeille : {best_bee.path}")

    return b, best_distance, avg_history, best_history


if __name__ == "__main__":
    b, best_distance, avg_history, best_history = main(comments=True)

    # Les graphes sont produits par le fichier visualization.py
    viz = Visualization(b)
    viz.plot_evolution(best_history, avg_history)
    viz.plot_best_path()
    viz.plot_genealogy()