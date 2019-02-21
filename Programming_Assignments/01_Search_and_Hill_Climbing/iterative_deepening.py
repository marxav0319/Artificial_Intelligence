
import sys
import argparse
import copy

from state import State

def iterative_deepening_depth_first_search(file_path):
    """
    """

    initial_state = State.load_from_file(file_path)

    for depth in xrange(initial_state.minimum_tasks_needed, len(initial_state.tasks) + 1):
        state = depth_limited_search(initial_state, depth, 0)
        if state != None:
            return state

    return None

def depth_limited_search(state, depth, current_task):
    """
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