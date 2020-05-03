import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance_fast
import functools, glob, random, sys, os, time
import random


def prune_vertices_rec(G, T, min_pairwise_distance, depth=5):
    if depth == 0:
        return T, min_pairwise_distance
    best_T = T
    for vertex in T.nodes():
        # Need this check since we reassign best_T within the loop
        if not best_T.has_node(vertex):
            continue
        if len(best_T[vertex]) == 1:
            T_copy = best_T.copy()
            T_copy.remove_node(vertex)
            if is_valid_network(G, T_copy):
                pairwise_distance = average_pairwise_distance_fast(T_copy)
                if pairwise_distance < min_pairwise_distance:
                    best_T, min_pairwise_distance = T_copy, pairwise_distance
    best_T, min_pairwise_distance = prune_vertices_rec(G, best_T, min_pairwise_distance, depth - 1)

    return T, min_pairwise_distance


def prune_vertices_iter(G, T, depth):
    min_pairwise_distance = average_pairwise_distance_fast(T)
    for _ in range(depth):
        for vertex in T.nodes:
            if len(T[vertex]) == 1:
                T_copy = T.copy()
                T_copy.remove_node(vertex)
                if is_valid_network(G, T_copy):
                    pairwise_distance = average_pairwise_distance_fast(T_copy)
                    if pairwise_distance < min_pairwise_distance:
                        T, min_pairwise_distance = T_copy, pairwise_distance
    return T



def min_spt(G, pruner_depth):
    T = nx.minimum_spanning_tree(G)
    # T_curr, _ = prune_vertices_rec(G, T, average_pairwise_distance_fast(T), pruner_depth)
    T = prune_vertices_iter(G, T, T.number_of_nodes())
    min_cost = average_pairwise_distance_fast(T)
    for vertex in G.nodes():
        length, all_paths = nx.single_source_dijkstra(G, vertex)
        T_curr = nx.Graph()
        for vertex in G.nodes():
            T_curr.add_node(vertex)
        for path in all_paths.values():
            for i in range(len(path) - 1):
                T_curr.add_edge(path[i], path[i + 1], weight=G[path[i]][path[i + 1]]["weight"])

        start = time.time()
        T_curr, _ = prune_vertices_rec(G, T_curr, average_pairwise_distance_fast(T_curr), pruner_depth)
        # print(f'prune rec took {time.time() - start}')
        start = time.time()
        T_curr = prune_vertices_iter(G, T_curr, T_curr.number_of_nodes()//2)
        # print(f'prune iter took {time.time() - start}')


        cost = average_pairwise_distance_fast(T_curr)
        if cost < min_cost:
            min_cost, T = cost, T_curr

    return T, min_cost



def solve(G, pruner_depth=4):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    # Check if all vertices connected to 1
    for vertex in G.nodes():
        if len(list(G.neighbors(vertex))) == G.number_of_nodes() - 1:
            T = nx.Graph()
            T.add_node(vertex)
            return T

    #Find the minimum shortest paths tree
    start = time.time()
    T, min_pairwise_distance = min_spt(G, pruner_depth)
    print(f'min spt took {time.time() - start}')

    start = time.time()
    T, _ = prune_vertices_rec(G, T, min_pairwise_distance, pruner_depth)
    print(f'prune rec took {time.time() - start}')
    start = time.time()
    T = prune_vertices_iter(G, T, T.number_of_nodes())
    print(f'prune iter took {time.time() - start}')

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
        elif 'large' in path:
            T = solve(G, pruner_depth=4)
        else:
            T = solve(G, pruner_depth = 3)
        assert is_valid_network(G, T)
        graph_name = os.path.basename(path).split(".")[0]
        print(count, f"Average  pairwise distance for {graph_name}: {average_pairwise_distance_fast(T)}")
        count += 1
        write_output_file(T, os.path.join(output_dir, f"{graph_name}.out"))
