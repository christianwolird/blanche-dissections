import argparse
import logging
from pathlib import Path

from blanche.core.graph_utils import polyhedral_graphs_of_size
from blanche.core.algebra_utils import kirchhoff_ideal
from blanche.log_utils import setup_logging

logger = logging.getLogger(__name__)


def run_enumeration(args, results_file):
    """This is the core mathematical workflow."""
    logger.info("Enumerating Blanche dissections with %d rectangles...", args.n)

    graphs = polyhedral_graphs_of_size(
        args.n + 1, 
        no_duals=True,
        verbose=args.verbose
    )

    logger.info("Graph enumeration complete: found %d graphs in total.", len(graphs))

    for graph_id, graph in enumerate(graphs, start=1):
        edges = graph.edge_orbit_reps()

        logger.info("Graph #%d has %d types of edges.", graph_id, len(edges))
        results_file.write(f"Graph #{graph_id}: {graph.adj_dict}\n\n")

        for edge_id, edge in enumerate(edges, start=1):
            logger.debug("Checking edge #%d...", edge_id)
            results_file.write(f"Edge #{edge_id}: {edge}\n\n")
            
            K = kirchhoff_ideal(graph, edge)
            # Algebra will go here eventually.
            # Something like:
            # K = kirkhoff(graph, edge)
            # G = groebner(K)

        results_file.write("\n")

    logger.info("Enumeration finished.")



def main():
    args = parse_args()
    run_dir = configure_logging(args)

    results_path = run_dir / "dissections.txt"
    with results_path.open("w") as results_file:
        run_enumeration(args, results_file)


def parse_args():
    parser = argparse.ArgumentParser(
        description="enumerates Blanche dissections of a square with 'n' rectangles."
    )
    parser.add_argument("n", type=int, help="number of rectangles")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="print milestones throughout the computation",
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="print all information",
    )

    return parser.parse_args()


def configure_logging(args):
    console_level = logging.WARNING
    if args.verbose:
        console_level = logging.INFO
    if args.debug:
        console_level = logging.DEBUG

    run_dir = Path("results") / f"square_{args.n}_rect"
    run_dir.mkdir(parents=True, exist_ok=True)

    log_path = run_dir / "computation.log"

    setup_logging(log_path, console_level)

    return run_dir


if __name__ == "__main__":
    main()
