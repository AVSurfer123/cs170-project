import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import glob, random, sys, os

'''def solve_helper(G, T, considered_vertices):
    # Partition graph into 2 halves
    # Find the min cut across those 2 halves
    # Call solve helper recursively on the two haves
    # Add the min vertex back in
    if len(considered_vertices) < 2:
        return
    if len(considered_vertices) == 2:
        if G.has_edge(considered_vertices[0], considered_vertices[1]):
            T.add_node(considered_vertices[0])
            T.add_node(considered_vertices[1])
            T.add_edge(considered_vertices[0], considered_vertices[1], attr_dict = {'weight':G[considered_vertices[0]][considered_vertices[1]]['weight']})

    random.shuffle(considered_vertices)
    left, right = considered_vertices[:len(considered_vertices)//2], considered_vertices[len(considered_vertices)//2:]
    left_set, right_set = set(left), set(right)
    solve_helper(G, T, left)
    solve_helper(G, T, right)

    min_edge, min_weight = None, float('inf')
    for vertex in left_set:
        for adj_vertex in G.adj[vertex]:
            if adj_vertex in right_set and G[vertex][adj_vertex]['weight'] < min_weight:
                min_edge, min_weight = (vertex, adj_vertex), G[vertex][adj_vertex]['weight']

    if min_edge != None:
        T.add_node(min_edge[0])
        T.add_node(min_edge[1])
        T.add_edge(min_edge[0], min_edge[1], attr_dict = {'weight':min_weight})'''


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    '''T = nx.Graph()
    solve_helper(G, T, list(G.nodes))
    T = nx.minimum_spanning_tree(G)
    return T'''
    #Find the minimum shortest paths tree
    min_cost, min_length, min_path = float('inf'), [], []
    for vertex in G.nodes():
        length, path = nx.single_source_dijkstra(G, vertex)
        cost = 0
        for vertex_inner in G.nodes():
            cost += length[vertex_inner]
        if cost < min_cost:
            min_cost, min_length, min_path = cost, length, path.values()

    T = nx.Graph()
    for vertex in G.nodes():
        T.add_node(vertex)
    for path in min_path:
        for i in range(len(path) - 1):
            T.add_edge(path[i], path[i + 1], weight=G[path[i]][path[i + 1]]["weight"])

    #Prune the unecessary edges/vertices
    min_pairwise_distance = average_pairwise_distance_fast(T)
    for _ in range(10):
        for vertex in G.nodes():
            if not T.has_node(vertex):
                continue
            if len(T[vertex]) == 1:
                T_copy = T.copy()
                T_copy.remove_node(vertex)
                if is_valid_network(G, T_copy):
                    pairwise_distance = average_pairwise_distance_fast(T_copy)
                    if pairwise_distance < min_pairwise_distance:
                        T, min_pairwise_distance = T_copy, pairwise_distance
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
    for path in paths:
        G = read_input_file(path)
        T = solve(G)
        assert is_valid_network(G, T)
        graph_name = os.path.basename(path).split(".")[0]
        print(f"Average  pairwise distance for {graph_name}: {average_pairwise_distance(T)}")
        write_output_file(T, os.path.join(output_dir, f"{graph_name}.out"))
