# Python wrapper for nauty, the graph symmetry software.

import pynauty

def get_automorphism_generators(graph):
    g = pynauty.Graph(len(graph), adjacency_dict=graph)
    return pynauty.autgrp(g)[0]
