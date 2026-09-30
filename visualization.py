import matplotlib.pyplot as plt
import networkx as nx


class Visualization:
    '''
    Produit les 3 graphes demandés. Attend une ruche (Beehive) qui possède :
    - beehive.flowers : liste des coordonnées (x, y) des fleurs
    - beehive.queen   : la meilleure abeille (objet Bee avec path, bee_id, generation, parents)
    '''

    def __init__(self, beehive):
        self.beehive = beehive

    def plot_evolution(self, queen_distances, mean_distances):
        plt.figure(figsize=(9, 5))

        # Deux styles de trait différents : les courbes restent distinguables
        # même sans voir les couleurs (accessibilité)
        plt.plot(range(len(queen_distances)), queen_distances, label="Queen", linestyle="-")
        plt.plot(range(len(mean_distances)), mean_distances, label="Mean", linestyle="--")

        plt.xlabel("Generation")
        plt.ylabel("Distance")
        plt.title("Evolution of distances")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig("evolution.png", dpi=150)  # avant show(), sinon l'image est vide
        plt.show()
        plt.close()

    def plot_best_path(self):
        plt.figure(figsize=(8, 8))

        # Le chemin de la reine contient déjà la ruche au début et à la fin
        path = self.beehive.queen.path

        # Les fleurs : simples points
        flowers_x = [f[0] for f in self.beehive.flowers]
        flowers_y = [f[1] for f in self.beehive.flowers]
        plt.scatter(flowers_x, flowers_y, s=50, label="Flowers")

        # Le chemin : une ligne qui relie les points dans l'ordre de visite
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_x, path_y, linewidth=1, color="black", label="Path")

        # La ruche : point de départ, marqueur différent (hexagone)
        hive = path[0]
        plt.scatter(hive[0], hive[1], s=250, marker="h", zorder=3, label="Hive")

        plt.title("Best bee path")
        plt.legend()
        plt.savefig("best_path.png", dpi=150)
        plt.show()
        plt.close()

    def plot_genealogy(self, max_depth=5):
        '''
        Arbre généalogique de la reine.
        max_depth : nombre de niveaux d'ancêtres affichés (1 = parents, 2 = grands-parents...).
        Sans limite, l'arbre remonte jusqu'à la génération 0 et contient des centaines
        d'abeilles : illisible.
        '''
        plt.figure(figsize=(10, 8))

        genealogy = nx.DiGraph()
        queen = self.beehive.queen
        genealogy.add_node(queen.bee_id, generation=queen.generation)

        # On remonte niveau par niveau (parents, puis grands-parents...) depuis la reine
        seen = {queen.bee_id}
        current_level = [queen]
        for depth in range(max_depth):
            next_level = []
            for bee in current_level:
                if bee.parents is None:  # abeille de la génération 0 : pas de parents
                    continue
                for parent in bee.parents:
                    if parent.bee_id not in seen:
                        seen.add(parent.bee_id)
                        genealogy.add_node(parent.bee_id, generation=parent.generation)
                        next_level.append(parent)
                    genealogy.add_edge(parent.bee_id, bee.bee_id)
            current_level = next_level

        print("Genealogy bees:", genealogy.number_of_nodes())
        print("Genealogy relations:", genealogy.number_of_edges())

        # Une ligne par génération ; on inverse l'axe y pour avoir les plus anciennes en haut
        pos = nx.multipartite_layout(genealogy, subset_key="generation", align="horizontal")
        for node in pos:
            pos[node][1] *= -1

        # Position verticale de chaque génération (pour écrire son numéro à gauche)
        generation_positions = {}
        for node in genealogy.nodes:
            generation = genealogy.nodes[node]["generation"]
            generation_positions[generation] = pos[node][1]

        # Les abeilles
        nx.draw_networkx_nodes(genealogy, pos, node_size=30)

        # La reine, plus grosse, avec son étiquette
        queen_id = queen.bee_id
        nx.draw_networkx_nodes(genealogy, pos, nodelist=[queen_id], node_size=120)
        queen_x, queen_y = pos[queen_id]
        plt.text(queen_x + 0.05, queen_y, "Queen Bee", verticalalignment="center")

        # Les liens parent -> enfant, courbés pour ne pas se superposer.
        # Le tracé doit être DANS la boucle : sinon seule la dernière arête est dessinée.
        for parent, child in genealogy.edges():
            if pos[parent][0] < pos[child][0]:
                rad = 0.4
            else:
                rad = -0.4
            nx.draw_networkx_edges(genealogy, pos, edgelist=[(parent, child)],
                                   arrows=True, connectionstyle=f"arc3,rad={rad}")

        for generation, y in generation_positions.items():
            plt.text(-1.1, y, f"Generation {generation}",
                     horizontalalignment="right", verticalalignment="center")

        plt.xlim(-1.5, 1.1)
        plt.title(f"Genealogy of the best bee ({max_depth} levels of ancestors)")
        plt.savefig("genealogy.png", dpi=150)
        plt.show()
        plt.close()