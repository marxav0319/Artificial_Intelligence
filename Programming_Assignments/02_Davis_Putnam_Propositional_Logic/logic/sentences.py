from atom import Atom
from clause import Clause

class Sentences:
    """
    """

    def __init__(self, clauses):
        self.clauses = clauses
        self.compute_value()

    def compute_value(self):
        """
        """
        for clause in self.clauses:
            if clause.value == False:
                self.value = False
        self.value = True

    @classmethod
    def read_from_file(cls, filepath):
        """
        """
        clauses = []
        f = open(filepath)
        for line in f:
            clause = []
            if line[0] == '0':
                break
            else:
                line = line.strip().split(' ')
                for l in line:
                    clause.append(Atom(l))
            clauses.append(Clause(clause))
        return cls(clauses)

    def get_unique_atoms(self):
        """
        """
        atoms = []
        for clause in self.clauses:
            for atom in clause.atoms:
                if atom not in atoms:
                    atoms.append(atom)
        return atoms

    def _literal_counter(self, literals, atom):
        """
        """
        for entry in literals:
            if entry[0] == atom:
                if atom.string[0] == '-':
                    entry[1] = 1
                else:
                    entry[2] = 1

    def get_pure_literals(self):
        """
        """
        atoms = self.get_unique_atoms()
        literals = [[atom, 0, 0] for atom in atoms]

        # Walk through the atoms
        for clause in self.clauses:
            for atom in clause.atoms:
                self._literal_counter(literals, atom)

        pure_literals = [entry[0] for entry in literals if entry[1] == 0 or entry[2] == 0]
        return pure_literals

    def is_empty(self):
        """
        """
        return len(self.clauses) == 0

    def __str__(self):
        string = ''
        for clause in self.clauses:
            string += str(clause)
        return string