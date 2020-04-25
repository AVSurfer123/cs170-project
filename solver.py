import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import glob, sys, os


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
