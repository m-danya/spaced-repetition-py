import argparse

from spaced_repetition import storage
from spaced_repetition import cli

def main():
    parser = argparse.ArgumentParser(
        description='CLI for Spaced Repetition System')
    args = parser.parse_args()  
    storage.config.load_from_file()
    storage.cards.load_from_file()
    cli.main_loop()
    return


if __name__ == "__main__":
    main()