import networkx as nx
import matplotlib.pyplot as plt
from parse import read_input_file, read_output_file
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
    if len(sys.argv) == 3:
        mode = sys.argv[2]
    else:
        mode = 'input'
    if mode not in ['input', 'output']:
        print("Second argument must be whether it is an 'output' file.")
    if mode == 'output':
        name = path.split('/')[-1].split('.')[0]
        input_path = f'inputs/{name}.in'
        G = read_input_file(input_path)
        G = read_output_file(path, G)
    else:
        G = read_input_file(path)
    visualize_graph(G)
