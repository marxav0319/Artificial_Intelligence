class Value:
    """
    """

    def __init__(self, name, value, time, id):
        """
        """
        self.name = name
        self.value = value
        self.time = time
        self.id = id

    def __eq__(self, other):
        """
        """
        if type(self) != type(other):
            return False
        else:
            return ((self.name == other.name) and (self.value == other.value)
                    and (self.time == other.time))

    def __str__(self):
        return "ID %d: R%d = %s at time %d" % (self.id, self.name, self.value, self.time)