import sys

import front_end as fe
import davis_putnam as dp
import back_end as be

def print_usage():
    """
    """
    print "[*] ERROR: This script expected exactly 1 input: the filepath to the input file."
    print "Please ensure the input file exists (as a text file) and run again."
    print
    print "USAGE:"
    print "> python driver.py <filepath>"
    print "Exiting"
    sys.exit(1)

def main():
    """
    """
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print_usage()

    fe.front_end(sys.argv[1])
    dp.davis_putnam()
    be.back_end()

    return

if __name__ == '__main__':
    main()