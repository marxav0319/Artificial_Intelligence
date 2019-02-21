
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
        self.get_minimum_number_of_tasks_needed()
        self.compute_state()

    @staticmethod
    def read_file(file_path):
        file_handle = open(file_path)
        inputs = []
        for i in xrange(3):
            temp = file_handle.readline().strip().split(" ")
            inputs.append([float(element) for element in temp])
        file_handle.close()
        return inputs

    @classmethod
    def load_from_file(cls, file_path):
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
        tasks = sorted(self.tasks, reverse=True)
        min_num = 0
        current_index = 0
        while min_num < self.target:
            min_num += tasks[current_index].length
            current_index += 1
        self.minimum_tasks_needed = current_index

    def evaluate_processor_time_taken(self):
        for time_taken in self.processor_time_taken:
            if time_taken > self.deadline:
                return False
            return True 

    def evaluate_task_target(self):
        if self.target_progress >= self.target:
            return True
        return False

    def evaluate_state(self):
        assert(self.processor_time_taken != None)
        if self.evaluate_processor_time_taken() and self.evaluate_task_target():
            self.goal_state = True
        return self.goal_state
    
    def compute_state(self):
        self.processor_time_taken = [0 for i in xrange(len(self.processors))]
        self.target_progress = 0
        for task in self.tasks:
            if task.processor != None:
                ix = task.processor.index
                self.processor_time_taken[ix] += task.time_taken
                self.target_progress += task.length
        self.evaluate_state()

    def get_task_assignments(self):
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
