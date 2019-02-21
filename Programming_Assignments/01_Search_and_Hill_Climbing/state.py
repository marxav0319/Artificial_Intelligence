
class Processor:

    def __init__(self, index, speed):
        self.index = index
        self.speed = speed

    def __str__(self):
        return "Processor " + str(self.index) + " Speed: " + str(self.speed) + "\n"


class Task:

    def __init__(self, index, length):
        self.index = index
        self.length = length
        self.processor = None

    def assign_processor(self, processor):
        self.processor = processor
        self.time_taken = self.length / self.processor.speed

    def evaluate_task_time(self):
        if(self.processor != None):
            return self.time_taken

    def __str__(self):
        return ("Task " + str(self.index) + " Length: " + str(self.length)
                + " Assigned to " + str(self.processor) + "\n")


class State:

    def __init__(self, processors, tasks, deadline, target):
        self.processors = processors
        self.tasks = tasks
        self.deadline = deadline
        self.target = target
        self.goal_state = False
        self.processor_time_taken = None
        self.compute_state()
        self.evaluate_state()

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
        
        return cls(processors, tasks, parameters[0], parameters[1])
    
    def compute_state(self):
        self.processor_time_taken = [0 for i in xrange(len(self.processors))]
        self.target_progress = 0
        for task in self.tasks:
            if task.processor != None:
                ix = task.processor.index
                self.processor_time_taken[i] += task.time_taken
                self.target_progress += task.length

    def evaluate_processor_time_taken(self):
        for time_taken in self.processor_time_taken:
            if time_taken >= self.deadline:
                return False
            return True 

    def evaluate_task_target(self):
        if self.target_progress >= self.target:
            return True
        return False

    def write_goal_state(self):
        self.assignments = ""
        for task in self.tasks:
            self.assignments += (task.processor.index + " ")

        print self.assignments

    def evaluate_state(self):
        assert(self.processor_time_taken != None)
        if self.evaluate_processor_time_taken() and self.evaluate_task_target():
            self.goal_state = True
            return self.goal_state

    def __str__(self):
        print_str = "\nProcessors\n"

        for processor in self.processors:
            print_str += str(processor)

        print_str += "\nTasks\n"

        for task in self.tasks:
            print_str += str(task)

        return print_str

