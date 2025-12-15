import argparse

from blanche.graphs import enumerate_polyhedra_by_edges
from blanche.backends.nauty import edge_orbits


def main():
    parser = argparse.ArgumentParser()
    parser.description = "Enumerates Blanche dissections with 'n' rectangles."

    parser.add_argument(
        "n", 
        type=int, 
        help="number of rectangles"
    )
    
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="prints info throughout the computation"
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Enumerating Blanche dissections with {args.n} rectangles...")

    for graph in enumerate_polyhedra_by_edges(args.n+1, verbose=args.verbose):
        pass

if __name__ == "__main__":
    main()
