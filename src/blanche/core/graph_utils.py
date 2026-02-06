"""Utilities for graphs."""

import logging
import math

from blanche.backends.plantri import polyhedral_graphs_from_plantri 

logger = logging.getLogger(__name__)


def remove_duals(graphs):
    """
    Remove planar-dual duplicates from a list of graphs.
    
    Iterates in order and keeps the first member of each dual pair.
    """
    kept_graphs = []
    kept_duals = []

    for g in graphs:
        # Skip g if it matches the dual of a previously accepted graph.
        if any(g.is_isomorphic_to(d) for d in kept_duals):
            continue

        # Accept g and record its planar dual.
        kept_graphs.append(g)
        kept_duals.append(g.get_dual())

    return kept_graphs 


def polyhedral_graphs_of_size(E, *, verbose=False):
    """
    Yield polyhedral graphs with exactly E edges.

    Plantri's primary parameter is the number of vertices V, so we
    bound the possible number of vertices for a polyhedral graph with
    E edges and call plantri once for each V in that range.
    """

    V_min, V_max = _vertex_range_from_edge_count(E)

    logger.info("Enumerating polyhedral graphs with %d edges...", E)
    logger.info("Vertex range: %d <= V <= %d", V_min, V_max)

    graphs = []

    for V in range(V_min, V_max+1):
        logger.debug("Enumerating polyhedral graphs on %d vertices...", V)

        graphs_V = polyhedral_graphs_from_plantri(V, E)

        logger.debug("Found %d graphs with %d vertices.", len(graphs_V), V)

        graphs.extend(graphs_V)

    return graphs


def _vertex_range_from_edge_count(E):
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

