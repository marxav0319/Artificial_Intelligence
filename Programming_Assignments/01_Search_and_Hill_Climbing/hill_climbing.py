"""
hill_climbing.py

Holds the finished algorithm for iterative deepening depth first search using the state.State class.

Usage:
    The script expects to be run as __main__ with a passed text file.  The script can be run by
    navigating to the directory containing this script (along with the state.py file) and running:

    > python hill_climbing.py <file_path>.txt

    The given output will be either a list of processor assignments or "No solution".

Author: Mark Xavier (xaviem01)
"""

import argparse
from state import State

RANDOM_RESTART_LIMIT = 10

def hill_climbing_with_random_restart(file_name):
    """
    The function that actually carries out the hill climbing algorithm.

    Args:
        file_name <str>: the filepath + filename + file_extension for the input file from which
        to generate the state space.

    Returns:
        None: prints the solution of state.State.goal_state == True, else prints "No solution".
    """
    initial_state = State.load_from_file(file_name)
    current_best = initial_state

    for i in xrange(RANDOM_RESTART_LIMIT):
        if current_best.goal_state:
            break
        state_i = State.random_state_generator(initial_state)
        while True:
            best_neighbor = state_i.get_best_neighbor()
            if best_neighbor.cost == 0:
                state_i = best_neighbor
                break
            elif best_neighbor.cost < state_i.cost:
                state_i = best_neighbor
            else:
                break
        if state_i.cost < current_best.cost:
            current_best = state_i

    if current_best.goal_state:
        print current_best.get_task_assignments()
    else:
        print "No solution"

    return

def hill_climbing():
    """
    The main entry point for the hill climbing algorithm.
    """
    parser = argparse.ArgumentParser(description="Run iterative deepening")
    parser.add_argument('file_path', metavar="F", type=str,
                        help='The path to the file with the input data to read in.')
    args = parser.parse_args()
    result = hill_climbing_with_random_restart(args.file_path)

    return None

if __name__ == '__main__':
    hill_climbing()