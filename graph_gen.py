import random
import sys
import networkx as nx
import parse
import argparse

def generate_graph(num_vertices):
    G = nx.Graph()
    for i in range(num_vertices - 1):
        G.add_edge(i, i + 1, weight=round(random.uniform(0, 100), 3))
    for i in range(random.randrange(0, num_vertices)):
    	vertex1, vertex2 = random.randrange(0, num_vertices), random.randrange(0, num_vertices)
    	if vertex1 != vertex2 and not G.has_edge(vertex1, vertex2):
    		G.add_edge(vertex1, vertex2, weight=round(random.uniform(0, 100), 3))
    return G

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    G = generate_graph(int(sys.argv[1]))
    parse.write_input_file(G, sys.argv[2])
