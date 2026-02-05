**Status:** Under active development.

# Blanche Dissections

A toolkit for exploring dissections of surfaces into non-congruent equal-area rectangles. This includes a command-line tool `enumerate_dissections.py` to enumerate all such dissections of a square with a given number of rectangles.



## Quick Start

Enumerate Blanche dissections of a square into 7 rectangles:

```python
python enumerate_dissections.py 7 -v
```

This creates a directory:
```text
results/
  square_7_rect/
    results.txt
    computation.log
```

The file `results.txt` contains algebraic descriptions of the rectangle dimensions.
The file `computation.log` recordes the full enumeration process for verification.



## Prerequisites

You must have the graph enumeration software `plantri` available on your system. It must be installed separately.



## Installation

Clone the repository:

```bash
git clone https://github.com/christianwolird/blanche-dissections.git
cd blanche-dissections
```

Create and activate a virtual Python environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the `blanche` Python package:

```bash
pip install .
```

