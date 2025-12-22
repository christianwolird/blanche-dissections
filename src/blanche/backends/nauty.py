"""Python wrapper for nauty, the graph symmetry software."""

import pynauty

def get_automorphism_generators(graph):
    """
    Compute generators of the graph's automorphism group using nauty.

    Returns a list of vertex permutations. Each permutation is itself
    represented as list `p` where p[i] = j means `p` sends i to j.
    """
    g = pynauty.Graph(len(graph), adjacency_dict=graph)
    return pynauty.autgrp(g)[0]
