from atom import Atom

class Clause:
    """
    The Clause class - this class outlines what a single clause is.  A clause is a collection of
    atoms or a single atom.

    Args:
        atoms list(<atom.Atom>): the atoms that comprise the clause

    Returns:
        <clause.Clause>: the clause created by the disjunction of the atoms passed.  A valuation of
                         the clause is automatically computed to False if not all atoms are True).
    """

    def __init__(self, atoms):
        self.atoms = atoms
        self.compute_value()

    def update(self, atoms):
        """
        If a new set of atoms are passed, update the clause and re-compute the current value.  This
        function helps when an atom is passed an assignment.

        Args:
            atoms list<atom.Atom>: the updated atoms (with or without assignments)

        Returns:
            None
        """
        self.atoms = atoms
        self.compute_value()

    def is_empty(self):
        """Determines if this clause is empty."""
        return len(self.atoms) == 0

    def compute_value(self):
        """
        Computes the value of this clause.  If the clauses atoms are not all True (given their
        negation values) then the clause is False, else it is true.
        """
        self.value = False
        for atom in self.atoms:
            if atom.value == True:
                self.value = True
                break

    def remove(self, atom):
        """
        Given an atom to remove, remove it and create a new Clause instance to be passed back to the
        user for further processing.  Auto-computes the new valuation of the clause.

        Args:
            atom <atom.Atom>: the atom to remove from this clause.

        Returns:
            <clause.Clause>: a new Clause instance with the atom removed, along with a new valuation.
        """
        new_atoms = []
        for a in self.atoms:
            if a != atom:
                new_atoms.append(a)
        return Clause(new_atoms)

    def __str__(self):
        """A utility function for easy printing"""
        string = ''
        for atom in self.atoms:
            string += str(atom)
        string += '\n'
        return string

    def __contains__(self, atom):
        """
        A utility function to help ascertain if a certain atom exists in this clause.  The atom is
        checked regardless of its negation value (ie: if the atom is "42" then "-42" == "42" as
        well.)

        Args:
            atom <atom.Atom>: the atom to find

        Returns:
            <bool>: True if the atom is in this clause, else False.
        """
        if atom in self.atoms:
            return True
        return False

    def __len__(self):
        """
        Determine the number of atoms in this clause.

        Args:
            None

        Returns:
            <int>: the number of atoms in this clause.
        """
        return len(self.atoms)
