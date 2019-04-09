# Artificial Intelligence

## Programming Assignment 3

Author: Mark Xavier (xaviem01)

---

## Requirements:

* Python-2.7

---

## Contents:

```
03_Markov_Decisions
|
|-blackjack.py
|-README.md
|-README.html

```

---

## Usage

This script requires 3 command line arguments in order, the proper signature for calling this script
is noted below:

```shell
> # To run the program
>
> # All command line arguments passed are expected to be integers
> python blackjack.py <number-of-cards> <lower-score-target> <upper-score-target>
>
> # Example
> python blackjack.py 10 21 21
>
> # Sample output
Play Array
F T T T T T T T T T T T T T T T T T T T T
T F T T T T T T T T T T T T T T T T T T T
T T F T T T T T T T T T T T T T T T T T T
T T T F T T T T T T T T T T T T T T T T T
T T T T F T T T T T T T T T T T T T T T T
T T T T T F T T T T T T T T T T T T T T T
T T T T T T F T T T T T T T T T T T T T T
F T T T T T T F T T T T T T T T T T T T T
F F T T T T T T F T T T T T T T T T T T T
F F F T T T T T T F T T T T T T T T T T T
F F F F F T T T T T F T T T T T T T T T T
F F F F F F T T T T T F T T T T T T T T T
F F F F F F F T T T T T F T T T T T T T T
F F F F F F F F T T T T T F T T T T T T T
F F F F F F F F F F T T F F F T T T T T T
F F F F F F F F F F F F F F F F T T T T T
F F F F F F F F F F F F F F F F F T T T T
F F F F F F F F F F F F F F F F F F T T T
F F F F F F F F F F F F F F F F F F F T T
F F F F F F F F F F F F F F F F F F F F T
F F F F F F F F F F F F F F F F F F F F F

Prob Array
1.00 0.50 0.48 0.46 0.45 0.45 0.44 0.43 0.41 0.39 0.35 0.35 0.41 0.46 0.50 0.51 0.50 0.46 0.39 0.29 0.16
0.58 1.00 0.50 0.49 0.48 0.47 0.46 0.45 0.43 0.41 0.37 0.32 0.42 0.47 0.51 0.52 0.50 0.46 0.40 0.30 0.16
0.59 0.57 1.00 0.50 0.49 0.48 0.47 0.46 0.44 0.42 0.38 0.34 0.38 0.47 0.51 0.52 0.51 0.47 0.40 0.30 0.17
0.59 0.57 0.57 1.00 0.51 0.50 0.48 0.47 0.45 0.43 0.39 0.34 0.39 0.43 0.51 0.52 0.50 0.47 0.40 0.30 0.17
0.58 0.57 0.56 0.56 1.00 0.50 0.49 0.48 0.46 0.43 0.40 0.35 0.40 0.44 0.46 0.51 0.50 0.46 0.40 0.30 0.17
0.57 0.57 0.56 0.56 0.56 1.00 0.50 0.49 0.47 0.44 0.40 0.35 0.40 0.44 0.47 0.47 0.49 0.45 0.39 0.29 0.17
0.57 0.56 0.56 0.56 0.56 0.56 1.00 0.49 0.47 0.45 0.41 0.36 0.41 0.45 0.48 0.48 0.44 0.44 0.38 0.29 0.16
0.57 0.56 0.56 0.56 0.56 0.56 0.56 1.00 0.49 0.46 0.42 0.37 0.42 0.46 0.49 0.49 0.46 0.40 0.37 0.28 0.16
0.59 0.57 0.56 0.56 0.57 0.57 0.57 0.57 1.00 0.48 0.44 0.39 0.43 0.47 0.50 0.51 0.49 0.43 0.34 0.27 0.15
0.61 0.59 0.58 0.58 0.58 0.58 0.59 0.58 0.57 1.00 0.46 0.41 0.45 0.49 0.52 0.53 0.51 0.46 0.38 0.25 0.15
0.65 0.63 0.62 0.61 0.60 0.61 0.61 0.61 0.60 0.58 1.00 0.45 0.49 0.52 0.55 0.56 0.54 0.50 0.43 0.31 0.14
0.65 0.68 0.66 0.66 0.65 0.65 0.65 0.65 0.64 0.62 0.60 1.00 0.54 0.57 0.59 0.60 0.59 0.55 0.48 0.37 0.21
0.59 0.58 0.62 0.61 0.60 0.60 0.59 0.59 0.58 0.57 0.54 0.50 1.00 0.52 0.54 0.54 0.53 0.50 0.43 0.34 0.19
0.54 0.53 0.53 0.57 0.56 0.56 0.55 0.54 0.53 0.52 0.50 0.46 0.49 1.00 0.49 0.50 0.48 0.45 0.40 0.31 0.18
0.50 0.49 0.49 0.49 0.54 0.53 0.52 0.51 0.50 0.48 0.45 0.42 0.46 0.51 1.00 0.45 0.44 0.41 0.36 0.28 0.16
0.49 0.48 0.48 0.48 0.49 0.53 0.52 0.51 0.49 0.47 0.44 0.40 0.46 0.50 0.55 1.00 0.40 0.37 0.33 0.25 0.15
0.50 0.50 0.49 0.50 0.50 0.51 0.56 0.54 0.51 0.49 0.46 0.41 0.47 0.52 0.56 0.60 1.00 0.34 0.30 0.23 0.13
0.54 0.54 0.53 0.53 0.54 0.55 0.56 0.60 0.57 0.54 0.50 0.45 0.50 0.55 0.59 0.63 0.66 1.00 0.27 0.21 0.12
0.61 0.60 0.60 0.60 0.60 0.61 0.62 0.63 0.66 0.62 0.57 0.52 0.57 0.60 0.64 0.67 0.70 0.73 1.00 0.19 0.11
0.71 0.70 0.70 0.70 0.70 0.71 0.71 0.72 0.73 0.75 0.69 0.63 0.66 0.69 0.72 0.75 0.77 0.79 0.81 1.00 0.10
0.84 0.84 0.83 0.83 0.83 0.83 0.84 0.84 0.85 0.85 0.86 0.79 0.81 0.82 0.84 0.85 0.87 0.88 0.89 0.90 1.00

```
