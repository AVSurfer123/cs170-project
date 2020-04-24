import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import glob, sys


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    T = nx.minimum_spanning_tree(G)
    T_copy = T.copy()
    for node in T_copy.nodes():
        if len(list(T_copy.neighbors(node))) == 1:
        	try:
	            T.remove_edge(node, list(T_copy.neighbors(node))[0])
	            T.remove_node(node)
	        except:
	        	pass
    return T

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 3
    inputs = sys.argv[1]
    outputs = sys.argv[2]
    for path in glob.glob(inputs + "*.in"):
        G = read_input_file(path)
        T = solve(G)
        assert is_valid_network(G, T)
        try: 
            print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        except:
            print("Error")
        write_output_file(T, outputs + path[len(inputs):-2] + "out")
