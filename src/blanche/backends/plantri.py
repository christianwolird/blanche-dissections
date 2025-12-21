"""
Python wrapper for plantri, the graph enumeration software.

Call plantri to get all polyhedral graphs (up to isomorphism)
with a given number of vertices and edges.

Repackage plantri graphs as dictionaries {i:[neighbors of i]}
The list of neighbors is in rotational order and gives a planar embedding.
"""


import shutil
import subprocess


def parse_plantri_line(line):
    n_str, edge_info = line.split()
    num_vertices = int(n_str)

    neighborhoods = edge_info.strip().split(",")

    graph = dict()
    for i, nbhd_str in enumerate(neighborhoods):
        graph[i] = [ord(ch) - ord("a") for ch in nbhd_str]

    return graph


def call_plantri_polyhedra(V, E=None):
    """
    Call: plantri -p -c3 -a {V} -e{E}  
    Yield resulting graphs as dictionaries.
    """

    # Find plantri
    plantri_path = shutil.which("plantri")
    if plantri_path is None:
        raise RuntimeError("plantri not found")

    # Ask plantri for simple planar 3-connected graphs on 'V' vertices
    # in human-readable ASCII format,
    # optionally with exactly 'E' edges
    cmd = [plantri_path, "-p", "-c3", "-a"]
    cmd.append(str(V))
    if E is not None:
        cmd.append(f"-e{E}")

    # Run plantri.
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Iterate plantri's output as it runs.
    for line in proc.stdout:
        line = line.strip()
        if line:
            graph = parse_plantri_line(line)
            yield graph

    # Print any errors/crashes
    returncode = proc.wait()
    if returncode != 0:
        err = proc.stderr.read()
        raise RuntimeError(f"plantri failed (exit {returncode}):\n{err}")
