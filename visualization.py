import matplotlib.pyplot as plt
import networkx as nx


class Visualization:

    def __init__(self, beehive):
        self.beehive = beehive

    def plot_evolution(self, queen_distances, mean_distances):

        plt.plot(range(len(queen_distances)), queen_distances, label="Queen")
        plt.plot(range(len(mean_distances)), mean_distances, label="Mean")
        
        plt.xlabel("Generation")
        plt.ylabel("Distance")
        plt.title("Evolution of distances")
        plt.legend()
        plt.show() 


        
    def plot_best_path(self):
        route = [self.beehive.hive_node] + self.beehive.queen.path + [self.beehive.hive_node]
        route_edges = []
        for i in range(len(route)-1):
            route_edges.append((route[i], route[i + 1])) 
        pos = nx.get_node_attributes(self.beehive.graph, "pos")  

        nx.draw_networkx_nodes(self.beehive.graph, pos, nodelist=range(len(self.beehive.flowers)), node_size=50)     
        nx.draw_networkx_edges(self.beehive.graph, pos, edgelist=route_edges, width=1 )
        nx.draw_networkx_nodes(self.beehive.graph, pos, nodelist=[self.beehive.hive_node], node_size=250, node_shape="h")
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


        add_ancestors(self.beehive.queen)
        print("Genealogy bees:", genealogy.number_of_nodes())
        print("Genealogy relations:", genealogy.number_of_edges())
        
        
        pos = nx.multipartite_layout(genealogy, subset_key="generation", align="horizontal")
        for node in pos:
            pos[node][1] *= -1


        generation_positions = {}

        for node in genealogy.nodes:
            generation = genealogy.nodes[node]["generation"]
            generation_positions[generation] = pos[node][1]


        nx.draw(genealogy, pos, node_size=10)
        nx.draw_networkx_nodes(genealogy, pos, nodelist=[self.beehive.queen.bee_id], node_size=80)
        queen_id = self.beehive.queen.bee_id
        queen_x, queen_y = pos[queen_id]
        plt.text(queen_x + 0.05, queen_y, "Queen Bee", verticalalignment="center")
        
        
        edges = list(genealogy.edges())

        for parent, child in edges:
            if pos[parent][0] < pos[child][0]:
                rad = 0.4
            else:
                rad = -0.4

        nx.draw_networkx_edges(genealogy, pos, edgelist=[(parent, child)], arrows=True, connectionstyle=f"arc3,rad={rad}")    

        for generation, y in generation_positions.items():
            plt.text(-1.1, y, f"Generation {generation}",horizontalalignment="right",verticalalignment="center")
        
        plt.xlim(-1.5, 1.1)
        plt.title("Genealogy of the best bee")
        plt.show()

