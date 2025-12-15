import math

from blanche.backends.plantri import plantri_enumerate_polyhedra


def _vertex_range_from_edges(E):
    """
    Get upper and lower bound on the number of vertices
    in a polyhedral graph with a given number of edges.
    
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

        for graph in plantri_enumerate_polyhedra(V, E, verbose=verbose):
            yield graph
