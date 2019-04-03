"""
back_end.py

Holds the implementation of the back-end as described in programming assignment 2.  This script
converts the output of the davis_putnam algorithm to human-readable steps for assigning registers.

Author: Mark Xavier
"""

# Contants
INFILE = r'temp_outputs/davis_putnam_output'
ASSIGN_ATOM = 'A'
VALUE_ATOM = 'V'

def read_input_file():
    """
    Reads the output of davis_putnam.
    """
    true_atoms = []
    translations = []
    switch = False
    f = open(INFILE)
    for line in f:
        l = line.strip().split(" ")
        if l[0] == '0':
            switch = True
            continue
        elif switch == False and l[1] == 'T':
            true_atoms.append(l[0])
        else:
            if l[0] in true_atoms and l[1] == ASSIGN_ATOM:
                translations.append(l)
    f.close()
    return translations

def print_translations(translations):
    """
    Prints the back-translated solution given by davis-putnam to the screen.

    Args:
        translations list<str>: the true valued atoms computed from davis-putnam in the coded
                                form written by the front_end.

    Returns:
        None
    """
    print '\nSolution:'
    time = 0
    result = 'Cycle 1: '
    for t in translations:
        if time != int(t[4]):
            time = int(t[4])
            result += '\nCycle %d: ' % (time + 1) 
        result += 'R%s = R%s; ' % (t[2], t[3])
    print result
    print
    return

def back_end():
    """
    The main driver for the back-end.
    """

    # Simply read the input file, if we have no valuation, print no solution, else print valuation.
    translations = read_input_file()
    if len(translations) == 0:
        print '\nNo Solution\n'
    else:
        print_translations(translations)

    return

if __name__ == '__main__':
    back_end()