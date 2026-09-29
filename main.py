import csv
import statistics
from config import FLOWERS_PATH, NB_GENERATIONS, NB_SURVIVANT, NB_BEES, MUTATION_RATE
import matplotlib.pyplot as plt 

from beehive import Gen_evo
from beehive import Beehive


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


def main(verbose=True, plot=False, every=100):
    # verbose : affiche les résultats dans le terminal
    # every   : une ligne de progression toutes les 'every' générations
    flowers = load_data(FLOWERS_PATH)

    b = Beehive(flowers)
    bees = b.init_bees()
    g = Gen_evo()

    avg_history = []

    for i in range(NB_GENERATIONS):
        list_of_dist = b.compute_path(bees)
        avg_history.append(sum(list_of_dist) / len(list_of_dist))

        best_bees = g.selection(list_of_dist, bees, NB_SURVIVANT)
        nb_children = NB_BEES - len(best_bees)
        new_generation = g.crossover(best_bees, nb_children)
        new_generation = g.mutations(new_generation, MUTATION_RATE)
        bees = best_bees + new_generation

        # (i+1) % every == 0 : vrai seulement aux générations 100, 200, 300...
        if verbose and (i + 1) % every == 0:
            print(f"Génération {i+1} : distance moyenne = {avg_history[-1]:.1f}")

    final_dist = b.compute_path(bees)
    best_distance = min(final_dist)
    best_bee = bees[final_dist.index(best_distance)]

    if verbose:
        gain = (1 - avg_history[-1] / avg_history[0]) * 100  # baisse de la moyenne en %
        print("--- Résultats ---")
        print(f"Distance moyenne : {avg_history[0]:.1f} (gén. 1) -> {avg_history[-1]:.1f} (gén. {NB_GENERATIONS}), soit -{gain:.1f} %")
        print(f"Meilleure distance finale : {best_distance:.1f}")
        print(f"Trajet de la meilleure abeille : {best_bee}")

    if plot:
        plot_avg_history(avg_history)

    return best_distance

def benchmark(nb_essais=20):
    resultats = []
    for _ in range(nb_essais):
        # Chaque appel refait une simulation complète, sans affichage
        resultats.append(main(verbose=False, plot=False))
    print(f"moyenne = {statistics.mean(resultats):.0f}, "
          f"écart-type = {statistics.stdev(resultats):.0f}")


def plot_avg_history(avg_history):
    # Axe x : numéros de génération (1, 2, 3...), axe y : distance moyenne
    generations = range(1, len(avg_history) + 1)

    plt.figure(figsize=(9, 5))  # taille de la figure en pouces
    plt.plot(generations, avg_history)  # trace la courbe

    # Titres et légendes des axes (nécessaires pour que le graphe soit lisible seul)
    plt.title("Évolution du temps de parcours moyen par génération")
    plt.xlabel("Génération")
    plt.ylabel("Distance moyenne parcourue")

    plt.grid(True, alpha=0.3)  # quadrillage léger
    plt.savefig("avg_history.png", dpi=150)  # sauvegarde l'image (pour README et diapos)
    plt.show()  # affiche la fenêtre


if __name__ == "__main__":
    main(verbose=True, plot=True)
    # benchmark(nb_essais=20)  # ou main() pour une seule simulation