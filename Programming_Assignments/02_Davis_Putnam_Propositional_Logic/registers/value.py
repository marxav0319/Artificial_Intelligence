class Value:
    """
    The Value class - an atom for the front-end of this assignment.

    Args:
        name <int>: the register number as an int
        value <str>: the value at the register
        time <int>: the time at which this register holds this value
        id <int>: the id of this atom, used for conversion to for DP and back-conversion.

    Returns:
        <value.Value>: an instance of this class representing a register with a given value at a
                       given time.
    """

    def __init__(self, name, value, time, id):
        self.name = name
        self.value = value
        self.time = time
        self.id = id

    def __eq__(self, other):
        """
        A utility function to test if two atoms are the same regardless of their IDs.
        """
        if type(self) != type(other):
            return False
        else:
            return ((self.name == other.name) and (self.value == other.value)
                    and (self.time == other.time))

    def __str__(self):
        """ A utility function for easy printing. """
        return "R%d = %s at time %d" % (self.name, self.value, self.time)