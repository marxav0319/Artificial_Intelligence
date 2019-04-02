class Atom:
    """
    The atom class, this is a single atom for use in Davis-Putnam.  The atom has a string
    representation of itself along with an assignment, which is None, false, or true.

    Args:
        string <str>: the string representation of the atom, expected to be a string int with
                      (-) prepended for negation.

    Returns:
        <atom.Atom>: an atom with the string representation passed, a negation value (true or false),
                     and an assignment of [None, True, False].
    """

    def __init__(self, string):
        self.string = string
        self.assignment = None
        self.neg = True if self.string[0] == '-' else False
        self.compute_value()

    def compute_value(self):
        """
        If assignment has been given or computed, value is the assignment flipped if self.negation
        is True, else just assignment.  This computes the value of this particular atom given the
        assignment.

        Args:
            None

        Returns:
            None
        """
        if self.assignment != None:
            self.value = not self.assignment if self.neg == True else self.assignment
        else:
            self.value = False

    def assign(self, val):
        """
        A utility function for assignment.  First, pass val to assignment, then compute the value
        of the atom given the assignment and the value of self.negation.

        Args:
            val <bool>: True or False depending on the assignment chosen by Davis-Putnam

        Returns:
            None
        """
        self.assignment = val
        self.compute_value()

    def auto_assign(self):
        """
        Auto assigns the assignment of this atom to [True, False] given the value of negation
        (trying to make the atom True overall).  If Negation == True, then assign False so that the
        atom overall is True, else assign True.

        Args:
            None

        Returns:
            None
        """
        if self.neg == True:
            self.assignment = False
        else:
            self.assignment = True
        self.compute_value()

    def __str__(self):
        """
        A utility function for easy printing.
        """
        atom_str = self.string if self.string[0] != '-' else self.string[1:]
        return atom_str + ' ' + ('T' if self.assignment == True else 'F')

    def __eq__(self, other):
        """
        Equality test only tests if the atom number (the integer assigned) is equal to the other
        atom, not if the negation value is set or not.  Useful for list comparisons
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
