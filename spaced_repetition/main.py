import argparse
import sys
from spaced_repetition import storage


def main():
    parser = argparse.ArgumentParser(
        description='CLI for Spaced Repetition System')
    args = parser.parse_args()  
    storage.config.read_from_file()
    return 0


if __name__ == "__main__":
    sys.exit(main())