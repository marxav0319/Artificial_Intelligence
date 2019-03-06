"""
Holds the implementation of the Davis-Putnam algorithm defined in class.

Author: Mark Xavier
"""
import copy

from logic.sentences import Sentences

def dp1(atoms, sentences):
    """
    """
    i = 1
    while(True):
        print
        print "loop start", i
        print sentences, len(sentences.clauses)
        # The base case where we've satisfied all sentences
        if sentences.is_empty():
            print "Sentences are empty! Ending"
            for atom in atoms:
                if atom.assignment == None:
                    atom.assign(True)
            return atoms
        # The base case where we have found an invalid valuation of atoms
        elif sentences.contains_empty_clause():
            print "Empty clause found - return None"
            return None
        # Easy case with pure literal elimination
        elif len(sentences.get_pure_literals()) > 0:
            pure_literals = sentences.get_pure_literals()
            pure_literal = pure_literals[0]
            print 'Found pure literal', pure_literal
            for atom in atoms:
                if atom == pure_literal:
                    pure_literal.auto_assign()
                    atom.assign(pure_literal.assignment)
                    sentences.delete_clauses_containing_atom(atom)
                    break
        # Easy case with single literal clause
        elif sentences.contains_clause_with_single_literal():
            atom = sentences.assign_single_literal()
            print 'Found single literal', atom
            index = atoms.index(atom)
            atoms[index].assign(atom.assignment)
            sentences.propogate(atom, atom.assignment)
        # No more reductions are available
        else:
            break
        i += 1

    # The hard cases
    for i, atom in enumerate(atoms):
        if atom.assignment == None:
            print 'Found atom', atom, 'and assigning True'
            edit_atoms = copy.deepcopy(atoms)
            edit_atoms[i].assign(True)
            sentences_copy = copy.deepcopy(sentences)
            sentences_copy.propogate(edit_atoms[i], True)
            new_atoms = dp1(edit_atoms, sentences_copy)
            if new_atoms != None:
                return new_atoms
        if atom.assignment == None:
            print 'Found atom', atom, 'and assigning True'
            edit_atoms = copy.deepcopy(atoms)
            edit_atoms[i].assign(False)
            sentences_copy = copy.deepcopy(sentences)
            sentences_copy.propogate(edit_atoms[i], False)
            new_atoms = dp1(edit_atoms, sentences_copy)
            if new_atoms != None:
                return new_atoms

def davis_putnam():
    """
    """
    sentences = Sentences.read_from_file('test_inputs/input1')
    atoms = sentences.get_unique_atoms()
    pure_literals = sentences.get_pure_literals()

    atoms_assigned = dp1(atoms, sentences)
    if atoms_assigned == None:
        print 'No Solution'
    else:
        for atom in atoms_assigned:
            print atom

    return

if __name__ ==  '__main__':
    davis_putnam()
