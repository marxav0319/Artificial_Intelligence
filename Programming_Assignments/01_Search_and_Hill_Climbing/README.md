# Artificial Intelligence

## Programming Assignment 1

Author: Mark Xavier (xaviem01)

---

## Requirements:

* Python-2.7 (all imports are standard including `argparse`, `copy`, `random`, and `sys`).

---

## Contents:

* _iterative_deepening.py_ - Contains the entry-point and algorithm definition for iterative deepening.
* _hill_climbing.py_ - Contains the entry-point and algorithm definition for hill climbing.
* _state.py_ - Holds definition for the Processor, Task, and State classes used in the above two files.
* _README.md_ - Markdown for this README file.
* _README.html_ - HTML for this README file.

---

## Usage

The files iterative_deepening.py and hill_climbing.py hold the code that solves the assignment.  They
can be run directly from the shell, however both expect a command line argument denoting the text
file with the state space definition (the list of tasks, processors, and parameters).  In order to
run the code, first ensure that all 3 .py files are in the same directory (without any other files
that may cause name-clashing), then run:

```shell
> python iterative_deepening.py <filepath>
>
> # Or run
>
> python hill_climbing.py <filepath>

```

The output expected will either be processor assignments in the order of the tasks read in, or the
the printout "No solution":

```shell
> python iterative_deepening.py <filepath>
> 1 0 1 2
>
> # Or you might see
>
> python iterative_deepening.py <filepath>
> No solution
```
