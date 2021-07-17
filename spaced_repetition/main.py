import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()
    print('hi!')
    return 0


if __name__ == "__main__":
    sys.exit(main())
