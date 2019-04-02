class Assign:
    """
    The Assign class - an atom that represents assigning one register to the value held at another
    register at a given time.

    Args:
        reg1 <int>: the name of the left-hand side register
        reg2 <int>: the name of the right-hand side register
        time <int>: the time that this assignment occurs
        id <int>: a unique integer serving as an identifier for conversion for davis-putnam and for
                  back conversion.
    """

    def __init__(self, reg1, reg2, time, id):
        self.reg1 = reg1
        self.reg2 = reg2
        self.time = time
        self.id = id

    def __eq__(self, other):
        """
        A utility function to test if two assignment atoms are the same regardless of IDs.
        """
        if type(self) != type(other):
            return False
        else:
            return ((self.reg1 == other.reg1) and (self.reg2 == other.reg2)
                    and (self.time == other.time))

    def __str__(self):
        """ A utility function for easy printing. """
        return "R%d = R%d at time %d" % (self.reg1, self.reg2, self.time)