import math

from blanche.backends.plantri import call_plantri_polyhedra 
from blanche.backends.nauty import nauty_automorphism_generators


def enumerate_polyhedra_by_edges(E, *, verbose=False):
    """
    Enumerate polyhedral graphs with a given number of edges.

    Plantri enumerates primarily for a given number of vertices,
    not edges, so we bound the number of vertices
    and call Plantri once for each possibility.
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
            if verbose:
                print("    Found:", graph)
            yield graph


def unique_edges(graph):
    for orbit in edge_orbits(graph):
        yield orbit[0]


def edge_orbits(graph):
    aut_gens = nauty_automorphism_generators(graph)
    print('aut_gens =', aut_gens)
    return [[0], [1], [2]]


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


