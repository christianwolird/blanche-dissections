"""Central logging setup for Blanche."""

import logging
import sys


class AddTags(logging.Filter):
    def filter(self, record):
        record.leveltag = f"[{record.levelname}]" 
        record.moduletag = f"({record.module})" 
        return True

def setup_logging(log_path, console_level):
    """
    This function is called once by the top-level script. All modules then use
    `logging.getLogger(__name__)` and do not configure their own handlers.

    Policy:
        - Computation log records DEBUG and above (full calculation reconstruction).
        - Terminal output is controlled by a verbosity flag.
            * INFO and above for verbose runs.
            * WARNING and above for non-verbose runs.
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Clear existing handlers to avoid duplicate logs if this is called twice.
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)

    # Terminal output: human-readable progress and diagnostics.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    root_logger.addHandler(console_handler)

    # Ensure the log directory exists.
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # File output: full DEBUG-level trace for reconstruction.
    computation_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    computation_handler.setLevel(logging.DEBUG)
    computation_handler.addFilter(AddTags())
    computation_handler.setFormatter(
        logging.Formatter(
            "%(leveltag)-7s %(moduletag)-50s %(asctime)s\n"
            " ⤷ %(message)s"
        )
    )

    root_logger.addHandler(computation_handler)

