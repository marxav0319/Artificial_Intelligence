# Artificial Intelligence

## Programming Assignment 4

Author: Mark Xavier (xaviem01)

---

## Requirements:

* Python-2.7

---

## Contents:

```
04_Reinforcement_Learning
|
|-blackjack.py
|-README.md
|-README.html

```

---

## Usage:

The function can be called with the following signature (running the `-h` flag will also display
the output below):

```
> python blackjack.py -h

usage: blackjack.py [-h] [-v] [-e] N LTarget UTarget K M N_Games

Blackjack game as described in programming assignment 4 for Artificial
Intelligence with Prof. Davis at NYU, Spring 2019

positional arguments:
  N                    The highest value card
  LTarget              The lowest winning score
  UTarget              The highest winning score
  K                    The maximum number of cards that can be drawn per turn
  M                    A floating-point value
  N_Games              The number of games to play

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        run with increased console ouptut
  -e, --extra-verbose  runs per game console output
```

So then the script can be called as follows:

```
> # Run with N = 2, LTarget = 4, UTarget = 5, K = 1, M = 4.0, N_Games = 10,000
> python blackjack.py 2 4 5 1 4.0 10000

1 1 1 1
1 1 1 1
1 1 1 1
1 1 1 1

0.7361 0.3969 0.1302 0.0000
0.5000 0.8045 0.3730 0.0053
0.5000 0.9876 0.7325 0.5105
0.5000 1.0000 0.9786 0.9886
```

There are also extra optional flags for verbose outputs.  `-v` prints the win and lose arrays that
are internally tracked after printing out the output above.  The arrays are printed with index D = 1.
The `-e` option is an extra-verbose option, that also outputs the state of each game after running
each game and before clearing the state for the next game.

## Notes:

For some reason (perhaps due to the random number function) my values do not always converge near
the Professor's examples.  I've combed through and tried to deal with some cases.  Some are not
clear, for instance, in the event that both players pass, the game ends, but it's not clear who
wins if both players draw.  In such a case, a winner was picked arbitrarily, which may account for
some of the off numbers.

In other cases, certain states are never reached, therefore there are no probabilities or perfect
moves for these players - these are chosen arbitrarily with a win probability of 0.5.  In other words,
if we ever encounter `win[p1_score][p2_score][p2_drew][j] + lose[p1_score][p2_score][p2_drew][j] == 0`,
we assign this a probability of winning as 0.5. 
