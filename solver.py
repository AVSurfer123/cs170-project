import networkx as nx
from parse import read_input_file, write_output_file, write_input_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import functools, glob, random, sys, os


def prune_vertices_rec(G, T, min_pairwise_distance, depth=5):
    if depth == 0:
        return T, min_pairwise_distance
    for vertex in G.nodes():
        if not T.has_node(vertex):
            continue
        if len(T[vertex]) == 1:
            T_copy = T.copy()
            T_copy.remove_node(vertex)
            if is_valid_network(G, T_copy):
                pairwise_distance = average_pairwise_distance_fast(T_copy)
                if pairwise_distance < min_pairwise_distance:
                    min_pairwise_distance, T = pairwise_distance, T_copy
                rec_T, rec_pairwise_distance = prune_vertices_rec(G, T_copy, min_pairwise_distance, depth - 1)
                if rec_pairwise_distance < min_pairwise_distance:
                    min_pairwise_distance, T = rec_pairwise_distance, rec_T
    return T, min_pairwise_distance

def prune_vertices_deep(G, T):
    min_pairwise_distance = average_pairwise_distance_fast(T)
    change = True
    while change:
        change = False
        for vertex in G.nodes():
            if not T.has_node(vertex):
                continue
            if len(T[vertex]) == 1:
                T_copy = T.copy()
                T_copy.remove_node(vertex)
                if is_valid_network(G, T_copy):
                    pairwise_distance = average_pairwise_distance_fast(T_copy)
                    if pairwise_distance < min_pairwise_distance:
                        change = True
                        T, min_pairwise_distance = T_copy, pairwise_distance

def min_spt(G, pruner_depth):
    min_cost, T = float('inf'), None
    for vertex in G.nodes():
        length, all_paths = nx.single_source_dijkstra(G, vertex)
        T_curr = nx.Graph()
        for vertex in G.nodes():
            T_curr.add_node(vertex)
        for path in all_paths.values():
            for i in range(len(path) - 1):
                T_curr.add_edge(path[i], path[i + 1], weight=G[path[i]][path[i + 1]]["weight"])

        T
        T_curr, _ = prune_vertices_rec(G, T_curr, average_pairwise_distance_fast(T_curr), pruner_depth)
        prune_vertices_deep(G, T_curr)
        cost = average_pairwise_distance_fast(T_curr)

        if cost < min_cost:
            min_cost, T = cost, T_curr
    return T

'''def prune_vertices_push(G, T):
    for vertex in G.nodes():
        if not T.has_node(vertex):
            continue
        neighbors = G.neighbors(vertex)
        for neighbor in neighbors:
            if not T.has_node(neighbor):
                continue
            T_copy = T.copy()'''



def solve(G, pruner_depth=4):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    #All vertices connected to 1 check
    for vertex in G.nodes():
        if len(list(G.neighbors(vertex))) == G.number_of_nodes() - 1:
            T = nx.Graph()
            T.add_node(vertex)
            return T

    #Find the minimum shortest paths tree
    T = min_spt(G, pruner_depth)

    #Prune the unecessary edges/vertices
    #min_pairwise_distance = average_pairwise_distance_fast(T)
    #prune_vertices_push(G, T)
    #T, _ = prune_vertices_rec(G, T, min_pairwise_distance, pruner_depth)
    #prune_vertices_deep(G, T)
    return T

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 3
    inputs = sys.argv[1]
    output_dir = sys.argv[2]
    if os.path.isdir(inputs):
        paths = [os.path.join(inputs, file) for file in os.listdir(inputs)]
    elif '.in' in inputs:
        paths = [inputs]
    print(paths)
    count = 1
    for path in paths:
        G = read_input_file(path)
        if 'small' in path:
            T = solve(G, pruner_depth = 5)
        if 'large' in path:
            T = solve(G, pruner_depth = 2)
        else:
            T = solve(G, pruner_depth = 4)
        assert is_valid_network(G, T)
        graph_name = os.path.basename(path).split(".")[0]
        print(count, f"Average  pairwise distance for {graph_name}: {average_pairwise_distance(T)}")
        count += 1
        write_input_file(T, os.path.join(output_dir, f"{graph_name}.out"))
