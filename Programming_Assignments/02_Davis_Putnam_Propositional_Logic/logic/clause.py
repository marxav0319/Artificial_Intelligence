from atom import Atom

class Clause:
    """
    """

    def __init__(self, atoms):
        self.atoms = atoms
        self.compute_value()

    def update(self, atoms):
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

    def remove(self, atom):
        """
        """
        new_atoms = []
        for a in self.atoms:
            if a != atom:
                new_atoms.append(a)
        return Clause(new_atoms)

    def __str__(self):
        string = ''
        for atom in self.atoms:
            string += str(atom)
        string += '\n'
        return string

    def __contains__(self, atom):
        """
        """
        if atom in self.atoms:
            return True
        return False

    def __len__(self):
        """
        """
        return len(self.atoms)
