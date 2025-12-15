# Python wrapper for Plantri, the graph enumeration software.

import math
import shutil
import subprocess

def enumerate_polyhedra_by_edges(num_edges, *, verbose=False):
    if verbose:
        print(f"Enumerating polyhedral graphs with {num_edges} edges...")

    # Vertex upper bound proof:
    #   Vertices in a polyhedral graph have degree >= 3.
    #   --> 3V <= 2E
    #   -->  V <= 2E / 3
    max_vertices = math.floor( 2 * num_edges / 3)

    # Vertex lower bound proof:
    #   Polyhedral graphs satisfy Euler's formula.
    #   --> V - E + F = 2
    #   Each face in a polyhedral graph touches at least 3 edges.
    #   --> 3F <= 2E
    #   -->  F <= 2E / 3
    #   Putting these together:
    #   --> F = 2 - V + E <= 2E / 3
    #   --> V >= E / 3 + 2
    min_vertices = math.ceil(num_edges / 3 + 2)

    if verbose:
        print(f"Vertex range: {min_vertices} <= V <= {max_vertices}")

    for num_vertices in range(min_vertices, max_vertices+1):
        if verbose:
            print(f"  Checking graphs with {num_vertices} vertices...")

        for graph in enumerate_polyhedra_by_vertices(num_vertices, verbose=verbose):
            # TODO: test edge count
            yield graph

def enumerate_polyhedra_by_vertices(num_vertices, *, verbose=False):
    yield 'whattamellon'

