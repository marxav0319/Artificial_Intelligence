
class Processor:

    def __init__(self, index, speed):
        self.index = index
        self.speed = speed

    def __str__(self):
        return "Processor " + str(self.index) + " Speed: " + str(self.speed)


class Task:

    def __init__(self, length):
        self.length = length
        self.processor = None

    def assign_processor(processor):
        self.processor = processor
        self.time_taken = self.length / self.processor.speed

    def evaluate_task_time():
        if(self.processor != None):
            return self.time_taken


class State:

    def __init__(self, processors, tasks, deadline, target):
        self.processors = processors
        self.tasks = tasks
        self.deadline = deadline
        self.target = target
        self.goal_state = False
        self.processor_time_taken = None
    
    def compute_state():
        self.processor_time_taken = [0 for i in xrange(len(self.processors))]
        self.target_progress = 0
        for task in tasks:
            if task.processor != None:
                ix = task.processor.index
                self.processor_time_taken[i] += task.time_taken
                self.target_progress += task.length

    def evaluate_processor_time_taken():
        for time_taken in self.processor_time_taken:
            if time_taken >= self.deadline:
                return False
            return True 

    def evaluate_task_target():
        if self.target_progress >= self.target:
            return true
        return false

    def write_goal_state():
        self.assignments = ""
        for task in self.tasks:
            self.assignments += (task.processor.index + " ")

        print self.assignments

    def evaluate_state():
        assert(self.processor_time_taken != None)
        if evaluate_processor_time_taken() and evaluate_task_target():
            self.goal_state = True
            write_goal_state()

    def __str__(self):
        print_str = "\nProcessors\n"

        for processor in self.processors:
            print_str += ("Processor " + str(processor.index) + " Speed: " + str(processor.speed) + "\n")

        print_str += "\nTasks\n"

        for i, task in enumerate(self.tasks):
            print_str += ("Task " + str(i) + " Length: " + str(task.length)
                          + " Assigned to Processor: " + str(task.processor) + "\n")

        return print_str

