import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import glob, sys
import numpy as np
import os.path
from os import path


def single_source_dij(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    #MST base
    if len(G.nodes())==1:
        return G
    
    short = nx.Graph()
    span = dict(nx.all_pairs_dijkstra(G))
    nodes = G.nodes()
    
    best_node = -1
    best_value = -1
        
                    
    for i in range(len(nodes)):
        path_lengths = list(span[i][1].values())
        summed_avg = max([len(x) for x in path_lengths])
        
        
        if best_value < 0 or summed_avg < best_value:
            best_value = summed_avg
            best_node = i
    
    #add all shortest paths from node that yields lowest average shortest path to all other nodes
    paths = list(span[i][1].values())
    
    for p in paths:
        counter = 0
        while counter < len(p) - 1:
            if not short.has_edge(p[counter], p[counter+1]):
                short.add_edge(p[counter], p[counter+1], weight=G[p[counter]][p[counter+1]]['weight'])
        
            counter+=1
    
    
    
    ####Code below prunes degree 1 nodes from tree if it helps
    nodes_span = list(short.nodes())
    degree_nodes = [i[1] for i in short.degree(nodes_span)]
    
    for i in range(len(degree_nodes)):
        if degree_nodes[i] == 1 and short.number_of_nodes() > 1:
            short.remove_node(nodes_span[i])

    edges_span = [edge for edge in short.edges()]
    avg_pair = average_pairwise_distance(short)

    for e in G.edges():
        if not short.has_edge(e[0], e[1]):
            new_dist = None
            copied = short.copy()
            copied.add_edge(e[0], e[1])
            if is_valid_network(G, copied):
                new_dist = average_pairwise_distance(copied)
            if not new_dist == None and new_dist <= avg_pair and is_valid_network(G, copied):
                avg_pair = new_dist
                short.add_edge(e[0], e[1])
   
        
        
    return short
