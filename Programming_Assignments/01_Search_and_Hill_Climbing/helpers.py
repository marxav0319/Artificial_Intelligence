
def get_input(filePath):

    file_handle = open(filePath)
    inputs = []
    for i in xrange(3):
        temp = file_handle.readline().strip().split(" ")
        inputs.append([float(element) for element in temp])

    file_handle.close()
    return inputs
