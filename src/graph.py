import networkx as nx
import numpy as np
import random

class QuantumGraph(nx.Graph):
    @staticmethod
    def gen_random(n : int) -> nx.Graph:
        """
        entry :
            n: int, the number of nodes we want.
        output :
            a random graph of size n.
        """
        if n <= 0:
            raise ValueError("The number of nodes must be a positive integer.")
        g = QuantumGraph(format="png")

        for i in range(n):
            g.add_node(i)

        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    g.add_edge(i, j)

        return g

    def show_coloring(self, m : np.matrix):
        """
        Displays the graph with its nodes colored based on a binary coloring matrix.

        Parameters:
            m : np.matrix
                A binary coloring matrix (N x K) where:
                - N is the number of nodes.
                - K is the number of colors.
                - m[i, j] = 1 indicates that node i is assigned color j.
        """
        import matplotlib.pyplot as plt

        if not isinstance(m, np.matrix):
            raise ValueError("The coloring matrix must be a numpy matrix.")

        num_nodes, num_colors = m.shape
        if num_nodes != len(self.nodes):
            raise ValueError("The number of nodes in the coloring matrix must match the number of nodes in the graph.")

        color_map = []
        for i in range(num_nodes):
            color_index = np.argmax(m[i])
            color_map.append(color_index)

        pos = nx.spring_layout(self)
        nx.draw(self, pos, node_color=color_map, with_labels=True, cmap=plt.cm.rainbow, node_size=500, font_color='white')
        plt.show()

    def adjacency_matrix(self) -> np.matrix:
        nodes = self.nodes()

        adjacency_matrix = np.zeros((len(nodes), len(nodes)))

        node_index = {node: idx for idx, node in enumerate(nodes)}

        for edge in self.edges():
            i, j = node_index[edge[0]], node_index[edge[1]]
            adjacency_matrix[i][j] = 1
            adjacency_matrix[j][i] = 1
        
        return adjacency_matrix