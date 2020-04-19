import networkx as nx
import matplotlib.pyplot as plt
from parse import read_input_file
import sys

def visualize_graph(G):
    nx.draw_networkx(G)
    plt.show()

if __name__ == '__main__':
    path = sys.argv[1]
    G = read_input_file(path)
    visualize_graph(G)
