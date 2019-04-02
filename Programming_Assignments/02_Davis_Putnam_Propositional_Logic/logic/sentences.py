from atom import Atom
from clause import Clause
import copy

class Sentences:
    """
    The Sentences class is a collection clause.Clause classes.  An instance of Sentences has it's
    own value (whether the collection of Clauses themselves are True) and is used for the
    Davis-Putnam algorithm.

    Args:
        clauses list(<clause.Clause>): the list of clause.Clause values to initialize the Sentences
                                       class with.
        rest_of_input <str>: after encountering a "0" in the input-file, pass the rest of the file
                             in as this string.

    Returns:
        <sentences.Sentences>: an instance of the sentences class with its own valuation and a list
                               of clauses.
    """

    def __init__(self, clauses, rest_of_input):
        self.clauses = clauses
        self.rest_of_input = rest_of_input
        self.compute_value()

    def update(self, clauses):
        """
        Given a new set of clauses, assign those clauses to this instance of Sentences and re-compute
        the valuation of this instance.

        Args:
            clauses list(<clause.Clause>): the updated list of Clauses.

        Returns:
            None
        """
        self.clauses = clauses
        self.compute_value()

    def compute_value(self):
        """
        Computes the valuation of this instance given the cumulative valuation of each clause in
        this instance.
        """
        for clause in self.clauses:
            if clause == [] or clause.value == False:
                self.value = False
        self.value = True

    @classmethod
    def read_from_file(cls, filepath):
        """
        Create an instance of Sentences from an input file.  This file format is given by the
        professor for this class.

        Args:
            filepath <str>: the filepath to the input file.

        Returns:
            <sentences.Sentences>: an instance of the Sentences class with the given clauses in the
                                   input file.
        """
        clauses = []
        f = open(filepath)

        # First read in the clauses
        for line in f:
            clause = []
            if line[0] == '0':
                break
            else:
                line = line.strip().split(' ')
                for l in line:
                    clause.append(Atom(l))
            clauses.append(Clause(clause))

        # Then read in the rest of the input file for the translation
        rest_of_input = []
        for line in f:
            rest_of_input.append(line)
        return cls(clauses, rest_of_input)

    def get_unique_atoms(self):
        """
        Given the clauses in this instance of sentences, compute a list of unique atoms between the
        clauses (ignore negation values).

        Args:
            None

        Returns:
            list(<atom.Atom>): the unique atoms between all clauses in this instance of Sentences.
        """
        atoms = []
        for clause in self.clauses:
            for atom in clause.atoms:
                if atom not in atoms:
                    atoms.append(atom)

        return atoms

    def _literal_counter(self, literals, atom):
        """
        A utility function to help determine if a given atom is a pure literal.  This function
        simply determines whether we've encountered a positive or negative value of the literal,
        and marks which has been encountered thus far.

        Args:
            literals list<list<atom.Atom, int, int>>: Given that this is supposed to be a hidden
                                                      function, I'll leave this without explaining.

        Returns:
            None
        """
        for entry in literals:
            if entry[0] == atom:
                if atom.string[0] == '-':
                    entry[1] = 1
                else:
                    entry[2] = 1

    def get_pure_literals(self):
        """
        Computes the list of pure literals between all clauses in this instance of Sentences.  A
        pure literal is a literal that exists between all clauses in this instance as either only
        negated, or only non-negated.

        Args:
            None

        Returns:
            list<atom.Atom>: the list of pure literals.
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
        """ Returns whether or not the list is empty as a boolean. """
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
        Returns whether or not a given clause in this instance of Sentences is empty as a bool.
        """
        for clause in self.clauses:
            if clause.is_empty():
                return True

        return False

    def contains_clause_with_single_literal(self):
        """
        Returns whether or not a given clause contains only a single literal in this instance of
        Sentences as a bool.
        """
        for clause in self.clauses:
            if len(clause) == 1:
                return True
        return False

    def assign_single_literal(self):
        """
        Finds a single literal and auto-assigns a valuation to that single literal.
        """
        for clause in self.clauses:
            if len(clause) == 1:
                atom = clause.atoms[0]
                atom.auto_assign()
                return atom
        return None

    def propogate(self, atom, assignment):
        """
        Given an atom and it's assignment, searches through all clauses in this instance of Sentences
        and updates the valuation of that atom.  For an atom A, if ~A and A == False in a given clause,
        or if A and A == True remove that clause.  Else, if A and A == False, or if ~A and A == True,
        remove A from the given clause.  Then recompute the valuation of this instance of sentences.

        Args:
            atom <atom.Atom>: the atom to propogate on
            assignment <bool>: the assignment of the atom

        Returns:
            None
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
        """ A utility function for easy printing """
        string = ''
        for clause in self.clauses:
            string += str(clause)
        return string

    def __len__(self):
        """ A utility function to determine the number of clauses in this instance """
        return len(self.clauses)