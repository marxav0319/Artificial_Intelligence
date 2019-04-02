import copy
import sys
import os
from registers import Value, Assign

OUTFILE = r'temp_outputs/clauses.txt'
OUTFILE_T = r'temp_outputs/clauses_real.txt'

def split_names_and_values(start):
    """
    """
    names = [int(start[i]) for i in xrange(0, len(start), 2)]
    values = [start[i] for i in xrange(1, len(start), 2)]
    return names, values

def generate_value_atoms(start, time):
    """
    """
    regs, values = split_names_and_values(start)
    id = 1
    all_value_atoms = []
    for i in xrange(0, time+1):
        for reg_name in regs:
            for value in values:
                all_value_atoms.append(Value(reg_name, value, i, id))
                id += 1

    return all_value_atoms

def generate_assignment_atoms(start, time, last_id):
    """
    """
    regs = split_names_and_values(start)[0]
    id = last_id + 1
    all_assignment_atoms = []

    for i in xrange(0, time):
        for reg_1 in regs:
            for reg_2 in regs:
                if reg_1 != reg_2:
                    all_assignment_atoms.append(Assign(reg_1, reg_2, i, id))
                    id += 1

    return all_assignment_atoms


def read_input(filepath):
    """
    """
    f = open(filepath)
    start_state = f.readline().strip().split(" ")
    end_state = f.readline().strip().split(" ")
    time = int(f.readline().strip())
    f.close()

    return start_state, end_state, time


def generate_value_clauses(start, all_value_atoms, time=0):
    """
    """
    clause = ''
    verbose_clause = ''
    for i in xrange(0, len(start), 2):
        atom = all_value_atoms[all_value_atoms.index(Value(int(start[i]), start[i+1], time, 0))]
        clause += str(atom.id) + '\n'
    return clause


def generate_axiom_1_clauses(names, values, all_value_atoms, time):
    """
    Unique value axiom
    """
    clause = ''
    verbose_clause = ''
    for t in xrange(0, time+1):
        for name in names:
            for i in xrange(len(values)):
                for j in xrange(i+1, len(values)):
                        temp_register_1 = Value(name, values[i], t, 0)
                        temp_register_2 = Value(name, values[j], t, 0)
                        temp_1_index = all_value_atoms.index(temp_register_1)
                        temp_2_index = all_value_atoms.index(temp_register_2)

                        clause += "-%d -%d\n" % (all_value_atoms[temp_1_index].id,
                                                 all_value_atoms[temp_2_index].id)
    return clause


def generate_axiom_2_clauses(names, values, value_atoms, assign_atoms, time):
    """
    Positive effects of actions axiom
    """
    clause = ''
    for atom in assign_atoms:
        assign_time = atom.time
        assign_lhs = atom.reg1
        assign_rhs = atom.reg2

        for value in values:
            temp_assigner = Value(assign_rhs, value, assign_time, 0)
            temp_result = Value(assign_lhs, value, assign_time + 1, 0)
            temp_assigner_index = value_atoms.index(temp_assigner)
            temp_result_index = value_atoms.index(temp_result)

            clause += "%d -%d -%d\n" % (value_atoms[temp_result_index].id,
                                      value_atoms[temp_assigner_index].id,
                                      atom.id)
    return clause


def generate_axiom_3_clauses(names, values, value_atoms, assign_atoms, time):
    """
    Frame axiom
    """
    clause = ''
    for name in names:
        for value in values:
            for t in xrange(time):
                start_atom = Value(name, value, t, 0)
                end_atom = Value(name, value, t+1, 0)
                clause += "-%d %d" % (value_atoms[value_atoms.index(start_atom)].id,
                                      value_atoms[value_atoms.index(end_atom)].id)

                relevant_assign = [atom for atom in assign_atoms if atom.reg1 == name and atom.time == t]
                for atom in relevant_assign:
                    clause += " %d" % (atom.id)
                clause += "\n"
    return clause

def generate_axiom_4_clauses(names, values, value_atoms, assign_atoms, time):
    """
    Incompatible assignment axiom
    """
    clause = ''
    for atom in assign_atoms:
        lhs = atom.reg1
        rhs = atom.reg2
        assign_time = atom.time

        relevant_atoms = [a for a in assign_atoms if a.time == assign_time and
                          (a.reg1 == rhs or (a.reg1 == lhs and a.reg2 != rhs))]
        for assignment in relevant_atoms:
            clause += "-%d -%d\n" % (atom.id, assignment.id)
    return clause

def generate_clauses(start, end, time, all_value_atoms, all_assignment_atoms):
    """
    """
    names, values = split_names_and_values(start)
    clauses = ''
    clauses += generate_value_clauses(start, all_value_atoms)
    clauses += generate_value_clauses(end, all_value_atoms, time)
    clauses += generate_axiom_1_clauses(names, values, all_value_atoms, time)
    clauses += generate_axiom_2_clauses(names, values, all_value_atoms, all_assignment_atoms, time)
    clauses += generate_axiom_3_clauses(names, values, all_value_atoms, all_assignment_atoms, time)
    clauses += generate_axiom_4_clauses(names, values, all_value_atoms, all_assignment_atoms, time)
    clauses += "0\n"

    return clauses

def write_clauses_to_file(clauses, all_atoms):
    """
    """
    f = open(OUTFILE, 'w')
    f.write(clauses)
    for atom in all_atoms:
        if isinstance(atom, Value):
            f.write("%d V %d %s %d\n" % (atom.id, atom.name, atom.value, atom.time))
        else:
            f.write("%d A %d %d %d\n" % (atom.id, atom.reg1, atom.reg2, atom.time))
    f.close()

def write_actual_clauses_to_file(clauses, all_atoms):
    """
    """
    f = open(OUTFILE_T, 'w')
    line_list = clauses.splitlines()
    for line in line_list:
        ids = line.strip().split(" ")
        for id in ids:
            prefix = ''
            temp = id
            if id[0] == '-':
                temp = id[1:]
                prefix = '-'
            for atom in all_atoms:
                if atom.id == int(temp):
                    f.write(prefix + str(atom) + '; ')
        f.write("\n")
    f.close()

def print_usage():
    """
    """
    print "[*] ERROR: This script expected exactly 1 input: the filepath to the input file."
    print "Please ensure the input file exists (as a text file) and run again."
    print
    print "USAGE:"
    print "> python front_end.py <filepath>"
    print "Exiting"
    sys.exit(1)

def front_end(input_file=None):
    """
    """
    if input_file == None:
        if len(sys.argv) < 2 or len(sys.argv) > 2:
            print_usage()
        else:
            input_file = sys.argv[1]

    start_state, end_state, time = read_input(input_file)
    all_value_atoms = generate_value_atoms(start_state, time)
    all_assignment_atoms = generate_assignment_atoms(start_state, time, all_value_atoms[-1].id)
    clauses = generate_clauses(start_state, end_state, time, all_value_atoms, all_assignment_atoms)
    write_clauses_to_file(clauses, all_value_atoms + all_assignment_atoms)

if __name__ == '__main__':
    front_end()
