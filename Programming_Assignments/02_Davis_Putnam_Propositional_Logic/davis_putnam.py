"""
Holds the implementation of the Davis-Putnam algorithm defined in class.

Author: Mark Xavier
"""

from logic.sentences import Sentences

def dp1(atoms, sentences):
    """
    """

    while(True):

        # The base case where we've satisfied all sentences
        if sentences.is_empty():
            for atom in atoms:
                if atom.assignment == None:
                    atom.assign(True)
            return atoms
        # The base case where we have found an invalid valuation of atoms
        else:
            for clause in sentence:
                if clause.is_empty():
                    return None

        # Easy case with pure literal elimination



def davis_putnam():
    """
    """
    sentences = Sentences.read_from_file('test_inputs/input1')
    atoms = sentences.get_unique_atoms()
    pure_literals = sentences.get_pure_literals()

    print sentences
    print
    for atom in atoms:
        print atom
    print
    for atom in pure_literals:
        print atom

    return

if __name__ ==  '__main__':
    davis_putnam()
