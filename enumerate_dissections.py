import argparse
import logging
from pathlib import Path

from blanche.core.graph_utils import polyhedral_graphs_of_size
from blanche.log_utils import setup_logging

logger = logging.getLogger(__name__)


def run_enumeration(args):
    """This is the core mathematical workflow."""
    logger.info("Enumerating Blanche dissections with %d rectangles...", args.n)

    graphs = polyhedral_graphs_of_size(
        args.n + 1, 
        no_duals=True,
        verbose=args.verbose
    )
    logger.info("Graph enumeration complete: found %d graphs in total.", len(graphs))

    logger.info("Removing duals...")

    unique_graphs = remove_duals(graphs)
    logger.info("Only %d graphs remain after removing duals.", len(unique_graphs))

    for graph in unique_graphs:
        unique_edges = graph.edge_orbit_reps()
        logger.info("Current graph has %d unique edge types", len(unique_edges))


def main():
    args = parse_args()
    logger = configure_logging(args)
    run_enumeration(args)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Enumerates Blanche dissections with 'n' rectangles."
    )
    parser.add_argument("n", type=int, help="number of rectangles")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="prints info throughout the computation",
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="enables full debug output",
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


if __name__ == "__main__":
    main()
