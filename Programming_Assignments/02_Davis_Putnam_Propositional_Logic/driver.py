"""
driver.py

Runs front_end, davis_putnam, and back_end in one script in case the user does not want to run
each individually.

Author: Mark Xavier
"""

import sys

import front_end as fe
import davis_putnam as dp
import back_end as be

def print_usage():
    """
    Self-explanatory
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
    The main driver.
    """
    # File checking
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print_usage()

    # Run the front-end, davis-putnam, and back-end
    fe.front_end(sys.argv[1])
    dp.davis_putnam()
    be.back_end()

    return

if __name__ == '__main__':
    main()