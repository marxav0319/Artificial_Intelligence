INFILE = r'temp_outputs/davis_putnam_output.txt'
ASSIGN_ATOM = 'A'
VALUE_ATOM = 'V'

def read_input_file():
    """
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
    """
    print '\nAssignments:'
    for t in translations:
        print "R%s = R%s at Time: %s" % (t[2], t[3], t[4])
    return

def back_end():
    """
    """
    translations = read_input_file()
    if len(translations) == 0:
        print '\nNo Solution'
    else:
        print_translations(translations)

    return

if __name__ == '__main__':
    back_end()