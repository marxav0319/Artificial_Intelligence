from registers import Register

def read_input(filepath):
    f = open(filepath)
    start_state = f.readline().strip().split(" ")
    end_state = f.readline().strip().split(" ")
    time = int(f.readline().strip())
    f.close()

    value_atoms = []
    for i in xrange(0, len(start_state), 2):
        value_atoms.append(Register(start_state[i], start_state[i+1]))

    for i in xrange(0, len(end_state), 2):
        value_atoms.append(Register(end_state[i], end_state[i+1], time))

    return value_atoms

def main():
    start_end_states = read_input('test_inputs/fe_input_1')
    

if __name__ == '__main__':
    main()
