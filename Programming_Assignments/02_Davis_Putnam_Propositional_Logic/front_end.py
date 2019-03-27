import copy
from registers import Value, Assign

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


def generate_value_clauses(start, all_value_atoms):
    """
    """
    clause = ''
    for i in xrange(0, len(start), 2):
        atom = all_value_atoms[all_value_atoms.index(Value(int(start[i]), start[i+1], 0, 0))]
        clause += str(atom.id) + '\n'
    return clause


def generate_axiom_1_clauses(names, values, all_value_atoms, time):
    """
    """
    clause = ''
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


def generate_clauses(start, end, time, all_value_atoms, all_assignment_atoms):
    """
    """
    names, values = split_names_and_values(start)
    clauses = ''
    clauses += generate_value_clauses(start, all_value_atoms)
    clauses += generate_value_clauses(end, all_value_atoms)
    clauses += generate_axiom_1_clauses(names, values, all_value_atoms, time)
    clauses += generate_axiom_2_clauses(names, values, all_value_atoms, all_assignment_atoms, time)
    print clauses
    return


def main():
    start_state, end_state, time = read_input('test_inputs/fe_input_1')
    all_value_atoms = generate_value_atoms(start_state, time)
    all_assignment_atoms = generate_assignment_atoms(start_state, time, all_value_atoms[-1].id)
    generate_clauses(start_state, end_state, time, all_value_atoms, all_assignment_atoms)


if __name__ == '__main__':
    main()
