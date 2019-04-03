# Artificial Intelligence

## Programming Assignment 2

Author: Mark Xavier (xaviem01)

---

## Requirements:

* Python-2.7

---

## Contents:

```
02_Davis_Putnam_Propositional_Logic
|
|-front_end.py
|-davis_putnam.py
|-back_end.py
|-driver.py
|
|-logic
| |
| |-atom.py
| |-clause.py
| |-sentences.py
|
|-registers
| |
| |-assign.py
| |-value.py
|
|-temp_outputs

```

---

## Usage

This set of scripts can be run in two ways, either by running the front-end, davis-putnam, and the
back-end individually, or by running the provided driver program.  The front-end takes in a filename
as a command-line argument, then outputs to the temp-outputs folder.  The davis-putnam algorithm must
be run after the front-end, and reads in from the temp-outputs directory.  It also writes it's output
to that directory, which is then read in by the backend.  See examples on running below.

```shell
> # To run the driver program
>
> python driver.py <filepath>
>
> # Or these can be run individually
>
> python front_end.py <filepath>
> python davis_putnam.py
> python back_end.py
```

__NOTE:__  `davis_putnam.py` and `back-end.py` rely on the output stored in `temp-outputs` from
`front_end.py`, in order to get the correct results the script must be run in the order listed above.
