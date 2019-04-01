class Atom:
    """
    """

    def __init__(self, string):
        self.string = string
        self.assignment = None
        self.neg = True if self.string[0] == '-' else False
        self.compute_value()

    def compute_value(self):
        """
        """
        if self.assignment != None:
            self.value = not self.assignment if self.neg == True else self.assignment
        else:
            self.value = False

    def assign(self, val):
        self.assignment = val
        self.compute_value()

    def auto_assign(self):
        """
        """
        if self.neg == True:
            self.assignment = False
        else:
            self.assignment = True
        self.compute_value()

    def __str__(self):
        atom_str = self.string if self.string[0] != '-' else self.string[1:]
        return atom_str + ' ' + ('T' if self.assignment == True else 'F')

    def __eq__(self, other):
        """
        Equality test only tests if the atom number (the integer assigned) is equal to the other
        atom, not if the negation value is set or not.
        """
        if type(self) != type(other):
            return False
        else:
            lhs = self.string
            rhs = other.string
            if self.string[0] == '-':
                lhs = self.string[1:]
            if other.string[0] == '-':
                rhs = other.string[1:]
            return lhs == rhs
