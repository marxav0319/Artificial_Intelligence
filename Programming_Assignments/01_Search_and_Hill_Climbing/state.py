"""
state.py

Holds the definitions for the following classes:

Processor - a wrapper to hold processor indices and speeds

Task - a wrapper to hold task indices, processor assignments, lengths, and update methods for time
       taken to complete the given task with the given processor.

State - holds a list of state.Processor and state.Task, along with deadline and target values, then
        computes the current state given task assignments and determines cost and whether the
        current instance of state.State is a goal state.

Author: Mark Xavier (xaviem01)
"""

import random
import copy
import sys

class Processor:
    """
    The Processor Class

    This class serves as a wrapper for the processor speeds given in the input.  This is mainly
    created to ease printing.

    Args:
        index <int>: The processor index is simply a unique record id, start at 0
        speed <int>: The speed of the processor, obtained from a text file

    Returns:
        <state.Processor>: An object initialised with the given arguments
    """

    def __init__(self, index, speed):
        self.index = index
        self.speed = speed

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.index == other.index and self.speed == other.speed

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        """ A convenience method for easy printing during debugging"""

        return "Processor " + str(self.index) + " Speed: " + str(self.speed)


class Task:
    """
    The Task Class

    This class serves as a wrapper for the task lengths given, and provides an interface for
    assigning tasks to processors.

    Args:
        index <int>: The task index is simply a unique record id, start at 0.
        length <int>: The length of time for the task - used to calculate whether the deadline has
                      been reached after processor assignment.

    Returns:
        <state.Task>: An object initialised with the given arguments
    """

    def __init__(self, index, length):
        self.index = index
        self.length = length
        self.processor = None
        self.time_taken = 0

    def assign_processor(self, processor):
        """
        Assigns a processor to the given task.  If the processor is not None, update time_taken,
        else set time_taken to 0.
        """
        self.processor = processor
        if processor != None:
            self.time_taken = self.length / self.processor.speed
        else:
            self.time_taken = 0

    def __lt__(self, other):
        return self.length < other.length

    def __str__(self):
        """ A convenience method for easy printing during debugging"""

        return ("Task " + str(self.index) + " Length: " + str(self.length)
                + " Assigned to " + str(self.processor))


class State:
    """
    The State Class

    Holds a state (a node really) encapsulating all current processors, tasks, task assignments,
    and parameters for deadlines and target lengths.  A new state can be created with data from an
    existing state, and upon creation a new state will automatically compute whether or not it is
    the goal state, along with any parameters necessary to determine if the goal state has been
    attained.

    Args:
        processors <list <state.Processor> >: A list of processors given by the input text file
        tasks <list <state.Task> >: A list of tasks given by the input text file
        deadline <int>: The deadline for the processors to finish their assigned tasks
        target <int>: The target is the minimum summed length of all assigned tasks in order for
                      the goal state to be reached.

    Returns:
        <state.State>: An object initialised with the given arguments with an auto-calculated data
                       member determining of the goal_state has been reached.
    """

    def __init__(self, processors, tasks, deadline, target):
        self.processors = processors
        self.tasks = tasks
        self.deadline = deadline
        self.target = target
        self.goal_state = False
        self.processor_time_taken = None
        self.cost = 0
        self.get_minimum_number_of_tasks_needed()
        self.compute_state()
        self.cost_function()

    @staticmethod
    def read_file(file_path):
        """
        A convenience method to read inputs from a text file
        """
        file_handle = open(file_path)
        inputs = []
        for i in xrange(3):
            temp = file_handle.readline().strip().split(" ")
            inputs.append([float(element) for element in temp])
        file_handle.close()
        return inputs

    @classmethod
    def load_from_file(cls, file_path):
        """
        A class method to create an instance from a text file
        """
        task_lengths, processor_speeds, parameters = State.read_file(file_path)
        tasks = []
        processors = []
        for index, length in enumerate(task_lengths):
            tasks.append(Task(index, length))

        for index, speed in enumerate(processor_speeds):
            processors.append(Processor(index, speed))
        
        processors.append(None)
        return cls(processors, tasks, parameters[0], parameters[1])

    def get_minimum_number_of_tasks_needed(self):
        """
        Determines the minimum number of tasks needed to meet the target length - used for
        iterative deepening to determine the initial depth to traverse
        """
        tasks = sorted(self.tasks, reverse=True)
        min_num = 0
        current_index = 0
        while min_num < self.target:
            min_num += tasks[current_index].length
            current_index += 1
        self.minimum_tasks_needed = current_index

    def evaluate_processor_time_taken(self):
        """ Determines if tasks assigned to processors complete within the deadline """
        for time_taken in self.processor_time_taken:
            if time_taken > self.deadline:
                return False
        return True 

    def evaluate_task_target(self):
        """ Determines if the target length has been met given tasks assigned to processors """
        if self.target_progress >= self.target:
            return True
        return False

    def evaluate_state(self):
        """ Determines if the goal state has been reached """
        assert(self.processor_time_taken != None)
        if self.evaluate_processor_time_taken() and self.evaluate_task_target():
            self.goal_state = True
        return self.goal_state
    
    def compute_state(self):
        """ Computes necessary variables to determine if the goal state has been reached """
        self.processor_time_taken = [0 for i in xrange(len(self.processors))]
        self.target_progress = 0
        for task in self.tasks:
            if task.processor != None:
                ix = task.processor.index
                self.processor_time_taken[ix] += task.time_taken
                self.target_progress += task.length
        self.evaluate_state()

    def get_task_assignments(self):
        """
        Returns a string of task to processor assignments.  If, for example, we are given 4 tasks
        and 3 processors, tasks will be printed in the order they are read in (left to right from
        the given text file).  However the actual task itself is not printed, but the processor
        index that was assigned to the task.  For example, given the output:

        > state.get_task_assignments()
        > 1 0 2 3

        The above indicates that task 1 was assigned to processor 1, task 2 to no processor, task
        3 to processor 2, and task 4 to processor 3.
        """
        self.assignments = ""
        for task in self.tasks:
            if task.processor != None:
                self.assignments += (str(task.processor.index + 1) + " ")
            else:
                self.assignments += "0 "

        return self.assignments

    def __str__(self):
        """
        The built in string method so you can call "print <State>".  This was used for debugging
        purposes but was left in just for completion.
        """
        print_str = "\nProcessors\n"

        for processor in self.processors:
            print_str += (str(processor) + "\n")

        print_str += "\nTasks\n"

        for task in self.tasks:
            print_str += (str(task) + "\n")

        print_str += "\nParameters\n"
        print_str += ("Deadline: " + str(self.deadline) + "\nTarget: " + str(self.target))

        print_str += "\n\nTask Assignments At This State\n"
        print_str += self.get_task_assignments()

        print_str += "\n\nHas The Goal State Been Reached: " 
        print_str += "Yes" if self.goal_state == True else "No"

        return print_str

    # This section holds code that helps with the hill-climbing algorithm---------------------------

    def cost_function(self):
        """
        Sets the total cost of the current state, defined as the amount of overflow for time taken
        compared to the deadline for each processor + the underflow of the target length of assigned
        tasks.
        """
        self.cost = 0
        for time_taken in self.processor_time_taken:
            overflow = time_taken - self.deadline
            self.cost += max(0, overflow)
        self.cost += max(0, (self.target - self.target_progress))

    @classmethod
    def random_state_generator(cls, initial_state):
        """ Generates and returns a random state from a given state """
        tasks = copy.deepcopy(initial_state.tasks)
        for i in xrange(len(tasks)):
            tasks[i].assign_processor(random.choice(initial_state.processors))
        return cls(initial_state.processors, tasks, initial_state.deadline, initial_state.target)

    def get_single_change_neighbors(self):
        """
        Computes the neighbors of the current state that can be found by assigning a given task
        a different processor (or no processor).  Returns a list of tasks.
        """
        tasks = copy.deepcopy(self.tasks)
        processors = copy.deepcopy(self.processors)
        neighbors = []
        for i in xrange(len(tasks)):
            for j in xrange(len(processors)):
                if tasks[i].processor != processors[j]:
                    temp = copy.deepcopy(tasks)
                    temp[i].assign_processor(processors[j])
                    neighbors.append(temp)
        return neighbors

    def get_swapped_neighbors(self):
        """
        Computes the neighbors of the current state that can be found by swapping the processors
        assigned to any two tasks.  Returns a list of tasks.
        """
        tasks = copy.deepcopy(self.tasks)
        neighbors = []
        for i in xrange(len(tasks)):
            for j in xrange(1, len(tasks)):
                if tasks[i].processor != tasks[j].processor:
                    temp = copy.deepcopy(tasks)
                    temp_processor = tasks[j].processor
                    temp[j].assign_processor(tasks[i].processor)
                    temp[i].assign_processor(temp_processor)
                    neighbors.append(temp)
        return neighbors

    def get_neighbors(self):
        """
        Using the previous methods get_single_change_neighbors() and get_swapped_neighbors(),
        combines both lists into one full list of neighbors and converts all list elements,
        which are of type <list <state.Task>> to the return type <list <state.State>>
        """
        single_swap = self.get_single_change_neighbors()
        double_swap = self.get_swapped_neighbors()
        neighbors = single_swap + double_swap
        for i in xrange(len(neighbors)):
            neighbors[i] = State(self.processors, neighbors[i], self.deadline, self.target)
        return neighbors

    def get_best_neighbor(self):
        """
        Given the neighbors from get_neighbors(), determines the neighbor with the lowest cost
        and returns that state.
        """
        neighbors = self.get_neighbors()
        best = neighbors[0]
        for neighbor in neighbors[1:]:
            if best.cost > neighbor.cost:
                best = neighbor
        return best
