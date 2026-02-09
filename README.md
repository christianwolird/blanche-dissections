**Status:** Under active development. Graph enumeration works, but the algebra is not implemented yet.

# Blanche Dissections

A research toolkit for exploring dissections of squares into non-congruent rectangles
of equal area (Blanche dissections).

This project provides a command line tool,

`enumerate_dissections.py`

which enumerates all such dissections of a square for a given number of rectangles.



## Quick Start

Enumerate Blanche dissections of a square into 11 rectangles:

```python
python enumerate_dissections.py 11
```

This creates a directory:
```text
results/
  square_11_rect/
    computation.log
    dissections.txt
```

The file `dissections.txt` contains algebraic descriptions of the dissections.
The file `computation.log` recordes the full enumeration process for verification.



## Installing `plantri` (prerequisite)

This project depends on `plantri`, a fast graph-enumeration program.

`plantri` is **not a Python package** and must be installed separately
and be available on your system `PATH`.

1. Download source from 
    [Brendan McKay's website](https://users.cecs.anu.edu.au/~bdm/plantri/):
    ```bash
    wget https://users.cecs.anu.edu.au/~bdm/plantri/plantri50.tar.gz
    ```

2. Extract and build:
    ```bash
    tar -xzf plantri50.tar.gz
    cd plantri50
    make
    ```

3. Install the executable on your system `PATH`, for example:
    ```bash
    sudo cp plantri /usr/local/bin/
    ```

4. Verify `plantri` installation:
    ```bash
    plantri -h
    ```

    You should see something like:

    ```bash
    >E Usage: plantri [-uagsETh -Ac#txm#P#bpe#f#qQ -odGVX -v] n [res/mod] [outfile]
    ```


## Installing this repository

1. Clone the repository:
    ```bash
    git clone https://github.com/christianwolird/blanche-dissections.git
    cd blanche-dissections
    ```

2. Create and activate a virtual Python environment (recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the `blanche` Python package:
    ```bash
    pip install .
    ```

4. Verify `blanche` installation:
    ```bash
    python3 enumerate_dissections.py -h
    ```
    You should see:
    ```bash
    usage: enumerate_dissections.py [-h] [-v] [-d] n

    enumerates Blanche dissections of a square with 'n' rectangles.

    positional arguments:
      n              number of rectangles

    options:
      -h, --help     show this help message and exit
      -v, --verbose  print milestones throughout the computation
      -d, --debug    print all information
    ```

