# CS 170 Project Spring 2020

We have 2 different solvers that perform slightly differently (efficiency and perfomance wise) on different graphs. Usage: `python3 scripts/solver.py inputs/ outputs/` or `python3 scripts/solver_ashwin.py inputs/ outputs/`. 

You'll only need to install networkx to work with the our code. For installation instructions, follow: https://networkx.github.io/documentation/stable/install.html. `pip install networkx`

Files:
- `scripts/parse.py`: functions to read/write inputs and outputs
- `scripts/solver.py`: where you should be writing your code to solve inputs
- `scripts/utils.py`: contains functions to compute cost and validate NetworkX graphs

When writing inputs/outputs:
- Make sure you use the functions `write_input_file` and `write_output_file` provided
- Run the functions `read_input_file` and `read_output_file` to validate your files before submitting!
- These are the functions run by the autograder to validate submissions

