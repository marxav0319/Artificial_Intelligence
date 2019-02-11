
import sys
import argparse

from helpers import get_input

def iterative_deepening(file_path):
    """
    """

    tasks, processors, parameters = get_input(file_path)

    return None

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