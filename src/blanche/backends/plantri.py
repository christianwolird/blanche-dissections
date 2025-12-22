"""
Python wrapper for plantri, the graph enumeration software.

This backend enumerates polyhedral graphs (simple, planar, 3-connected)
up to isomorphism using plantri, then converts the graphs to adjacency
dictionaries.

Plantri's `-a` flag means human-readable ASCII format.
Neighbors are listed in rotational order, giving a planar embedding.
"""


import shutil
import subprocess


def parse_plantri_line(line):
    """
    Parse a single line of plantri `-a` output, representing one graph.

    Returns a dictionary `graph` where graph[i] = [neighbors of i].
    Neighbors are listed in rotational order.
    """
    n_str, edge_info = line.split()
    num_vertices = int(n_str)

    neighborhoods = edge_info.strip().split(",")

    graph = dict()
    for i, nbhd_str in enumerate(neighborhoods):
        graph[i] = [ord(ch) - ord("a") for ch in nbhd_str]

    return graph


def call_plantri_polyhedra(V, E=None):
    """
    Enumerate polyhedral graphs with V vertices
    (and optionally E edges)

    This calls: 
        plantri -p -c3 -a V [-eE]

    Returns resulting graphs as adjacency dictionaries.
    """

    # Locate plantri executable.
    plantri_path = shutil.which("plantri")
    if plantri_path is None:
        raise RuntimeError("plantri not found")

    # Build plantri command.
    cmd = [plantri_path, "-p", "-c3", "-a"]
    cmd.append(str(V))
    if E is not None:
        cmd.append(f"-e{E}")

    # Launch plantri.
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Iterate plantri's output.
    for line in proc.stdout:
        line = line.strip()
        if line:
            graph = parse_plantri_line(line)
            yield graph

    # Check for errors or crashes.
    returncode = proc.wait()
    if returncode != 0:
        err = proc.stderr.read()
        raise RuntimeError(f"plantri failed (exit {returncode}):\n{err}")
