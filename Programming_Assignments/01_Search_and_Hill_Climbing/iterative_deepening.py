"""
iterative_deepening.py

Holds the finished algorithm for iterative deepening depth first search using the state.State class.

Usage:
    The script expects to be run as __main__ with a passed text file.  The script can be run by
    navigating to the directory containing this script (along with the state.py file) and running:

    > python iterative_deepening.py <file_path>.txt

    The given output will be either a list of processor assignments or "No solution".

Author: Mark Xavier (xaviem01)
"""

import sys
import argparse
import copy

from state import State

def iterative_deepening_depth_first_search(file_path):
    """
    The function that generates the initial state, determines the depths to travel to, and calls
    the depth limited search some number of times before exiting.

    Args:
        file_path <str>: filepath + filename + file_extension for state space generation.

    Returns:
        <state.State> if a goal state is reached, else None.
    """

    initial_state = State.load_from_file(file_path)

    for depth in xrange(initial_state.minimum_tasks_needed, len(initial_state.tasks) + 1):
        state = depth_limited_search(initial_state, depth, 0)
        if state != None:
            return state

    return None

def depth_limited_search(state, depth, current_task):
    """
    The depth first search called by the caller iterative deepening function.  This function runs
    depth first search to a certain depth and tests whether or not the goal state is reached once
    the depth is reached, if not we back out and continue deepening on other states/nodes.

    Args:
        state <state.State>: The state on which to attempt depth first search
        depth <int>: The depth to travel to
        current_task <int>: An integer index into the list of tasks held by the current state.  This
                            index determines which task we are currently attempting to assing to a
                            processor.

    Returns:
        state.State if a goal state is reached, else None.
    """

    if depth == 0:
        if state.goal_state:
            return state
        else:
            return None

    for processor in state.processors:
        tasks = copy.deepcopy(state.tasks)
        if processor == None:
            tasks[current_task].assign_processor(processor)
            new_state = State(state.processors, tasks, state.deadline, state.target)
            return_state = depth_limited_search(new_state, depth-1, current_task+1)
            if return_state != None:
                return return_state
        else:
            task_length = state.tasks[current_task].length
            processor_time = state.processor_time_taken[processor.index]

            if ((task_length / processor.speed) + processor_time) <= state.deadline:
                tasks[current_task].assign_processor(processor)
                new_state = State(state.processors, tasks, state.deadline, state.target)
                return_state = depth_limited_search(new_state, depth-1, current_task+1)
                if return_state != None:
                    return return_state

    return None


def iterative_deepening():
    """
    The main entry point for the iterative deepening algorithm.
    """

    parser = argparse.ArgumentParser(description="Run iterative deepening")
    parser.add_argument('file_path', metavar="F", type=str,
                        help='The path to the file with the input data to read in.')
    args = parser.parse_args()
    result = iterative_deepening_depth_first_search(args.file_path)

    if result != None:
        print result.get_task_assignments()
    else:
        print "No Solution"

if __name__ == '__main__':
    iterative_deepening()