"""
Python wrapper for nauty, the graph symmetry software.

Assumptions:
    - Input graphs are given as adjacency dictionaries. 
    - Vertices must be labeled 0 through n-1.
"""

import pynauty


def _to_nauty_graph(adj_dict):
    """Converts integer-labeled adjacency dict to a pynauty Graph."""
    return pynauty.Graph(len(adj_dict), adjacency_dict=adj_dict)


def is_isomorphic_nauty(adj_dict1, adj_dict2):
    """Test if two graphs are isomorphic using nauty."""
    nauty_graph2 = _to_nauty_graph(adj_dict1)
    nauty_graph1 = _to_nauty_graph(adj_dict2)
    return pynauty.isomorphic(nauty_graph1, nauty_graph2)


def automorphism_generators(adj_dict):
    """
    Compute generators of the graph's automorphism group using nauty.

    Returns a list of vertex permutations. Each permutation is itself
    represented as list `p` where p[i] = j means `p` sends i to j.
    """
    nauty_graph = _to_nauty_graph(adj_dict)
    return pynauty.autgrp(nauty_graph)[0]
