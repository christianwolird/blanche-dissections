# Blanche Dissections

A toolkit for exploring dissections into non-congruent equal-area rectangles (**Blanche dissections**). This includes:

1. A command-line tool to enumerate all such dissections of a square with a given number of rectangles, yielding exact algebraic descriptions of the rectangle dimensions rather than numeric approximations.
2. A visualization tool to render images of these dissections from the algebraic data.

---

## Prerequisites

- `plantri` — polyhedral graph enumeration
- `nauty` — graph automorphisms to avoid redundancy

## Installation

Clone the repository:

```bash
git clone https://github.com/christianwolird/blanche-dissections.git
cd blanche-dissections
```

### Python environment (recommended)

Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install this Python package

```bash
pip install .
```

