# Python wrapper for nauty, the graph symmetry software.

import pynauty

def nauty_automorphism_generators(graph):
    g = pynauty.Graph(len(graph), graph)
    return pynauty.autgrp(g)[0]
