from state import Processor, Task, State

def get_input(filePath):

    file_handle = open(filePath)
    inputs = []
    for i in xrange(3):
        temp = file_handle.readline().strip().split(" ")
        inputs.append([float(element) for element in temp])

    file_handle.close()
    return inputs

def load_data(filePath):

    task_lengths, processor_speeds, parameters = get_input(filePath)
    tasks = []
    processors = []
    for length in task_lengths:
        tasks.append(Task(length))

    for index, speed in enumerate(processor_speeds):
        processors.append(Processor(index, speed))

    initial_state = State(processors, tasks, parameters[0], parameters[1])

    return initial_state