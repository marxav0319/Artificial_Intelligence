"""
davis_putnam.py

Holds the implementation of the Davis-Putnam algorithm defined in class.

Author: Mark Xavier
"""
import copy

from logic import Sentences

INFILE = r'temp_outputs/clauses'
OUTFILE = r'temp_outputs/davis_putnam_output'

def dp1(atoms, sentences):
    """
    The davis-putnam helper algorithm as described by the professor and online.

    Args:
        atoms list<atom.Atom>: the list of unique atoms in the sentences
        sentences <sentence.Sentences>: the set of clauses

    Returns:
        list<atom.Atom> or None depending on whether a satisfying valuation is found.
    """
    while(True):
        # The base case where we've satisfied all sentences
        if sentences.is_empty():
            for atom in atoms:
                if atom.assignment == None:
                    atom.assign(True)
            return atoms
        # The base case where we have found an invalid valuation of atoms
        elif sentences.contains_empty_clause():
            return None
        # Easy case with pure literal elimination
        elif len(sentences.get_pure_literals()) > 0:
            pure_literals = sentences.get_pure_literals()
            pure_literal = pure_literals[0]
            for atom in atoms:
                if atom == pure_literal:
                    pure_literal.auto_assign()
                    atom.assign(pure_literal.assignment)
                    sentences.delete_clauses_containing_atom(atom)
                    break
        # Easy case with single literal clause
        elif sentences.contains_clause_with_single_literal():
            atom = sentences.assign_single_literal()
            index = atoms.index(atom)
            atoms[index].assign(atom.assignment)
            sentences.propogate(atom, atom.assignment)
        # No more reductions are available
        else:
            break

    # The hard cases
    for i, atom in enumerate(atoms):
        if atom.assignment == None:
            edit_atoms = copy.deepcopy(atoms)
            edit_atoms[i].assign(True)
            sentences_copy = copy.deepcopy(sentences)
            sentences_copy.propogate(edit_atoms[i], True)
            new_atoms = dp1(edit_atoms, sentences_copy)
            if new_atoms != None:
                return new_atoms
        if atom.assignment == None:
            edit_atoms = copy.deepcopy(atoms)
            edit_atoms[i].assign(False)
            sentences_copy = copy.deepcopy(sentences)
            sentences_copy.propogate(edit_atoms[i], False)
            new_atoms = dp1(edit_atoms, sentences_copy)
            return new_atoms

def write_assignments(atoms, rest_of_input):
    """
    Write the assignments given to the atoms to file for translation from the back-end.

    Args:
        atoms list<atom.Atom> or None: the atoms with their assignments or None if no assignment
                                       could be found.
        rest_of_input list<str>: the rest of the input from the front-end to help with back translation.
    """
    f = open(OUTFILE, 'w')
    if atoms != None:
        for atom in atoms:
            f.write(str(atom) + '\n')

    f.write('0\n')
    for translation in rest_of_input:
        f.write(translation)
    f.close()

def davis_putnam():
    """
    The main driver program that calls the davis_putnam helper program.
    """
    # Create our sentences and compute the unique atoms
    sentences = Sentences.read_from_file(INFILE)
    atoms = sentences.get_unique_atoms()

    # Run the algorithm and write the solution
    atoms_assigned = dp1(atoms, sentences)
    write_assignments(atoms_assigned, sentences.rest_of_input)

    return

if __name__ ==  '__main__':
    davis_putnam()
