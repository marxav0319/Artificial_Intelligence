from atom import Atom
from clause import Clause
import copy

class Sentences:
    """
    """

    def __init__(self, clauses):
        self.clauses = clauses
        self.compute_value()

    def update(self, clauses):
        """
        """
        self.clauses = clauses
        self.compute_value()

    def compute_value(self):
        """
        """
        for clause in self.clauses:
            if clause == [] or clause.value == False:
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

        # Read in the rest of the file and store so that it can be re-written
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

    def delete_clauses_containing_atom(self, atom):
        """
        """
        clauses_to_keep = []
        for clause in self.clauses:
            if atom not in clause:
                clauses_to_keep.append(clause)
        self.update(clauses_to_keep)

    def contains_empty_clause(self):
        """
        """
        for clause in self.clauses:
            if clause.is_empty():
                return True

        return False

    def contains_clause_with_single_literal(self):
        """
        """
        for clause in self.clauses:
            if len(clause) == 1:
                return True
        return False

    def assign_single_literal(self):
        """
        """
        for clause in self.clauses:
            if len(clause) == 1:
                atom = clause.atoms[0]
                atom.auto_assign()
                return atom
        return None

    def propogate(self, atom, assignment):
        """
        """
        clauses_to_keep = []
        for clause in self.clauses:
            if atom not in clause:
                clauses_to_keep.append(clause)
            else:
                for a in clause.atoms:
                    if a == atom:
                        if (not a.neg) and (atom.assignment == True):
                            continue
                        elif (a.neg) and (atom.assignment == False):
                            continue
                        elif (not a.neg) and (atom.assignment == False):
                            clauses_to_keep.append(clause.remove(a))
                        elif (a.neg) and (atom.assignment == True):
                            clauses_to_keep.append(clause.remove(a))
        self.update(clauses_to_keep)

    def __str__(self):
        string = ''
        for clause in self.clauses:
            string += str(clause)
        return string

    def __len__(self):
        return len(self.clauses)