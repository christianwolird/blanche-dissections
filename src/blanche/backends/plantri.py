"""
Python wrapper for Plantri, the graph enumeration software.

Call Plantri to generate all polyhedral graphs (up to isomorphism)
with a given number of vertices and edges.

Repackage Plantri results as Python dictionaries: {vertex:[neighbors]}
The list of neighbors is in rotational order and gives a planar embedding.
"""


import shutil
import subprocess

def parse_plantri_a_line(line):
    # TODO
    return dict()

def plantri_enumerate_polyhedra(V, E, *, verbose=False):
    # TODO
    for _ in range(3):
        yield parse_plantri_a_line("")

