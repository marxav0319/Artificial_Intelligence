
import sys
import argparse

from helpers import load_data

def iterative_deepening(file_path):
    """
    """

    initial_state = load_data(file_path)
    print initial_state

def main():
    """
    """

    parser = argparse.ArgumentParser(description="Run iterative deepening")
    parser.add_argument('file_path', metavar="F", type=str,
                        help='The path to the file with the input data to read in.')
    args = parser.parse_args()
    iterative_deepening(args.file_path)

if __name__ == '__main__':
    main()