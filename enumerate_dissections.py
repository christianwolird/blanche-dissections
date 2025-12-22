import argparse

from blanche.core.graphs import enumerate_polyhedra_by_edges, get_unique_edges 


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
         unique_edges = get_unique_edges(graph)
         if args.verbose:
             print(f"    Found a graph with {len(unique_edges)} unique edges.")


if __name__ == "__main__":
    main()
