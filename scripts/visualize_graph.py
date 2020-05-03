import networkx as nx
import matplotlib.pyplot as plt
from parse import read_input_file
import sys

def visualize_graph(G, round_labels=True):
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    if round_labels:
        for key in labels:
            labels[key] = round(labels[key])
    nx.draw_networkx_edge_labels(G, pos, labels)
    plt.show()

if __name__ == '__main__':
    path = sys.argv[1]
    G = read_input_file(path)
    visualize_graph(G)
