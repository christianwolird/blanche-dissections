"""Utilities for enumerating polyhedral graphs and edge orbits."""

import math

from blanche.backends.plantri import call_plantri_polyhedra 
from blanche.backends.nauty import get_automorphism_generators


def enumerate_polyhedra_by_edges(E, *, verbose=False):
    """
    Yield polyhedral graphs with exactly E edges.

    Plantri's primary parameter is the number of vertices V, so we
    bound the possible number of vertices for a polyhedral graph with
    E edges and call plantri once for each V in that range.
    """

    if verbose:
        print(f"Generating polyhedral graphs with {E} edges...")

    V_min, V_max = _vertex_range_from_edges(E)

    if verbose:
        print(f"Vertex range: {V_min} <= V <= {V_max}")

    for V in range(V_min, V_max+1):
        if verbose:
            print(f"  Generating polyhedral graphs on {V} vertices...")

        for graph in call_plantri_polyhedra(V, E):
            yield graph


def _vertex_range_from_edges(E):
    """
    Get upper and lower bound on the number of vertices
    in a polyhedral graph given the number of edges.
    
    Upper bound derivation:
        In a polyhedral graph, every vertex degree is at least three.
          ⇒ 3V <= (sum of all degrees) = 2E
          ⇒ V <= 2E/3

    Lower bound derivation:
        Each face touches at least three edges.
          ⇒ 3F <= (sum of all face sizes) = 2E
          ⇒ F <= 2E/3
        Polyhedral graphs satisfy Euler's formula.
          ⇒ V - E + F = 2
          ⇒ F = E - V + 2
        Putting these together.
          ⇒ E - V + 2 <= 2E/3
          ⇒ V >= E/3 + 2
    """

    V_max = math.floor( 2 * E / 3)
    V_min = math.ceil(E / 3 + 2)

    return V_min, V_max


def get_unique_edges(graph):
    """
    Pick one edge from each automorphism orbit.

    Returns a list of (i, j) with i < j.
    """
    return [min(orbit) for orbit in get_edge_orbits(graph)]


def get_edge_orbits(graph):
    """
    Yield edge-orbits under the graph's automorphism group.

    The backend returns generators of the automorphism group as
    permutations of vertices. The orbit is computed by picking a seed
    edge and doing a DFS with the generators.

    Returns a list of sets
    """
    aut_gens = get_automorphism_generators(graph)

    # Build the edge set.
    edges = set()
    for i in graph.keys():
        for j in graph[i]:
            edges.add((min(i,j), max(i,j)))

    visited = set()
    
    for edge in edges:
        if edge in visited:
            continue

        orbit = set()
        stack = [edge]
        visited.add(edge)

        # DFS over the orbit: apply each generator to each new edge.
        while stack:
            u = stack.pop()
            orbit.add(u)

            for aut in aut_gens:
                v = _edge_image(u, aut)
                if v not in visited:
                    visited.add(v)
                    stack.append(v)

        yield orbit

def _edge_image(edge, aut):
    """
    Apply vertex permutation `aut" to an edge.
    """
    i, j = edge
    i_, j_ = aut[i], aut[j]
    return (min(i_, j_), max(i_, j_))
