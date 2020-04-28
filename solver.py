import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import glob, sys


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
#    span_tree = nx.minimum_spanning_tree(G)
#    nodes_span = list(span_tree.nodes())
#
#    degree_nodes = [i[1] for i in span_tree.degree(nodes_span)]
#
#    for i in range(len(degree_nodes)):
#        if degree_nodes[i] == 1 and span_tree.number_of_nodes() > 1:
#            span_tree.remove_node(nodes_span[i])
#
#    edges_span = [edge for edge in span_tree.edges()]
#    avg_pair = average_pairwise_distance(span_tree)
#
#    for e in G.edges():
#        if not span_tree.has_edge(e[0], e[1]):
#            new_dist = None
#            copied = span_tree.copy()
#            copied.add_edge(e[0], e[1])
#            if is_valid_network(G, copied):
#                new_dist = average_pairwise_distance(copied)
#            if not new_dist == None and new_dist <= avg_pair and is_valid_network(G, copied):
#                avg_pair = new_dist
#                span_tree.add_edge(e[0], e[1])
#
#    if average_pairwise_distance(span_tree) <= nx.average_shortest_path_length(G):
#        return span_tree
#
#    #brute force
#    new_graph = G.copy()
#
#    def exhaustive_search(graph):
#        if is_valid_network(G, graph) and average_pairwise_distance(T) < nx.average_shortest_path_length(G):
#            return graph
    def _expand(G, explored_nodes, explored_edges):
        """
        Expand existing solution by a process akin to BFS.

        Arguments:
        ----------
        G: networkx.Graph() instance
            full graph

        explored_nodes: set of ints
            nodes visited

        explored_edges: set of 2-tuples
            edges visited

        Returns:
        --------
        solutions: list, where each entry in turns contains two sets corresponding to explored_nodes and explored_edges
            all possible expansions of explored_nodes and explored_edges

        """
        frontier_nodes = list()
        frontier_edges = list()
        for v in explored_nodes:
            for u in nx.neighbors(G,v):
                if not (u in explored_nodes):
                    frontier_nodes.append(u)
                    frontier_edges.append([(u,v), (v,u)])
                print("in")
        return zip([explored_nodes | frozenset([v]) for v in frontier_nodes], [explored_edges | frozenset(e) for e in frontier_edges])

    def find_all_spanning_trees(G, root=0):
        """
        Find all spanning trees of a Graph.

        Arguments:
        ----------
        G: networkx.Graph() instance
            full graph

        Returns:
        ST: list of networkx.Graph() instances
            list of all spanning trees

        """

        # initialise solution
        explored_nodes = frozenset([root])
        explored_edges = frozenset([])
        solutions = [(explored_nodes, explored_edges)]
        # we need to expand solutions number_of_nodes-1 times
        for ii in range(G.number_of_nodes()-1):
            print("Hi")
            # get all new solutions
            solutions = [_expand(G, nodes, edges) for (nodes, edges) in solutions]
            # flatten nested structure and get unique expansions
            solutions = set([item for sublist in solutions for item in sublist])

        return [nx.from_edgelist(edges) for (nodes, edges) in solutions]
        
    ST = find_all_spanning_trees(G)
    print(len(ST))
        
            
        
    return G


# Here's an example of how to run your solver.

# Usage: python3 solver.py inputs/ outputs/
if __name__ == '__main__':
#    assert len(sys.argv) == 3
#    inputs = sys.argv[1]
    inputs = "../inputs/"
#    outputs = sys.argv[2]
    outputs = "../outputs/"
    for path in glob.glob(inputs + "small-266.in"):
        G = read_input_file(path)
        T = solve(G)
        assert is_valid_network(G, T)
        try: 
            print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        except:
            print("Error")
        write_output_file(T, outputs + path[len(inputs):-2] + "out")
