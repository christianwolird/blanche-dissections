"""
Planar graph object.

Represents a graph with an adjacency dictionary which doubles as a rotation system.
    adj_dict[v] = [neighbors of the vertex v in rotational order]

This lets us build planar duals. 

It also supports finding automorphism-based edge orbits via the nauty backend.
"""

from blanche.backends.nauty import automorphism_generators, is_isomorphic_nauty


class PlanarGraph:
    def __init__(self, adj_dict):
        self.adj_dict = adj_dict

    def __str__(self):
        return str(self.adj_dict)

    def is_isomorphic_to(self, other):
        return is_isomorphic_nauty(self.adj_dict, other.adj_dict)

    def dual(self):
        """Construct the planar dual graph."""
        faces, boundary_of = self._faces_and_boundary_map()

        def reverse_dart(dart):
            u, v = dart
            return (v, u)

        dual_adj_dict = {}

        for face_id, face in enumerate(faces):
            dual_adj_dict[face_id] = []
            for dart in face:
                neighbor_face_id = boundary_of[reverse_dart(dart)]
                dual_adj_dict[face_id].append(neighbor_face_id)

        return PlanarGraph(dual_adj_dict)

    def _faces_and_boundary_map(self):
        """
        Compute all faces as cyclic lists of darts, and a lookup table telling
        which face each dart lies on.
        
        Handedness info:
            - Assume a clockwise interpretation of the rotations system `adj_dict`
            - The boundaries of the faces are iterated in clockwise order.
            - `boundary_of` returns the face on the left side of the dart.

        Returns:
            faces: list[face], where face is list[dart] and dart is (u, v)
            on_boundary_of: dict[dart, face_id]
        """
        # neighbor_index[v][u] = index of u in v's list of neighbors.
        neighbor_index = {}
        for v, neighbors in self.adj_dict.items():
            neighbor_index[v] = {u: i for i, u in enumerate(neighbors)}

        def next_neighbor(v, u):
            neighbors = self.adj_dict[v]
            i = neighbor_index[v][u]
            return neighbors[(i - 1) % len(neighbors)]
            # With CW rotation order, this traces face boundaries in CW order.
            # Using `(i + 1)` would trace face boundaries in CCW order instead.

        def next_boundary_dart(dart):
            u, v = dart
            return (v, next_neighbor(v, u))

        darts = [(u, v) for u, neighbors in self.adj_dict.items() for v in neighbors]

        faces = []
        boundary_of = {}    
        # boundary_of[(u,v)] = index of the face on the left of the dart (u,v).

        for start_dart in darts:
            if start_dart in boundary_of:
                continue

            face_id = len(faces)
            face = []

            dart = start_dart
            while dart not in boundary_of:
                boundary_of[dart] = face_id
                face.append(dart)
                dart = next_boundary_dart(dart)

            faces.append(face)

        return faces, boundary_of

    def edge_orbit_reps(self):
        """
        Pick one edge from each automorphism orbit.

        Returns a list of (u, v) with u < v.
        """
        return [min(orbit) for orbit in self.edge_orbits()]

    def edge_orbits(self):
        """
        Yield edge-orbits under the graph's automorphism group.

        The backend returns generators of the automorphism group as
        permutations of vertices. The orbit is computed by picking a seed
        edge and doing a DFS with the generators.

        Returns a list of sets
        """
        automorphisms = automorphism_generators(self.adj_dict)

        # Build the edge set.
        edges = set()
        for u in self.adj_dict.keys():
            for v in self.adj_dict[u]:
                edges.add((min(u,v), max(u,v)))

        visited = set()
        
        for seed_edge in edges:
            if seed_edge in visited:
                continue

            orbit = set()
            stack = [seed_edge]
            visited.add(seed_edge)

            # DFS over the orbit: apply each generator to each new edge.
            while stack:
                edge = stack.pop()
                orbit.add(edge)

                for aut in automorphisms:
                    edge_img = _edge_image(edge, aut)
                    if edge_img not in visited:
                        visited.add(edge_img)
                        stack.append(edge_img)

            yield orbit


def _edge_image(edge, aut):
    """
    Apply vertex permutation `aut` to an edge.

    Helper function for calculating edge orbits.
    """
    u, v = edge
    u_, v_ = aut[u], aut[v]
    return (min(u_, v_), max(u_, v_))

