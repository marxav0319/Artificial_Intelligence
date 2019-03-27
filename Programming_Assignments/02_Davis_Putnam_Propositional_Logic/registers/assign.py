
class Assign:
    """
    """

    def __init__(self, reg1, reg2, time, id):
        """
        """
        self.reg1 = reg1
        self.reg2 = reg2
        self.time = time
        self.id = id

    def __eq__(self, other):
        """
        """
        if type(self) != type(other):
            return False
        else:
            return ((self.reg1 == other.reg1) and (self.reg2 == other.reg2)
                    and (self.time == other.time))

    def __str__(self):
        """
        """
        return "R%d = R%d at time %d" % (self.reg1, self.reg2, self.time)