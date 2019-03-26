class Register:
    """
    """

    def __init__(self, name, value, time=0):
        self.name = int(name)
        self.value = value
        self.time = time

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        else:
            return self.name == other.name

    def __str__(self):
        return "R%d = %s at time %d" % (self.name, self.value, self.time)