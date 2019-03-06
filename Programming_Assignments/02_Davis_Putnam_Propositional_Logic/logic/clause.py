from atom import Atom

class Clause:
    """
    """

    def __init__(self, atoms):
        self.atoms = atoms
        self.compute_value()

    def is_empty(self):
        return len(self.atoms) == 0

    def compute_value(self):
        """
        """
        self.value = False
        for atom in self.atoms:
            if atom.value == True:
                self.value = True
                break

    def __str__(self):
        string = ''
        for atom in self.atoms:
            string += str(atom)
        string += '\n'
        return string