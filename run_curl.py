#!/usr/bin/python3
from argparse import ArgumentParser
import os

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Run curl', add_help=False)
    arg_parser.add_argument('-u', '--uri', dest='uri', action='store',
            required=True, help='URI to request')
    settings = arg_parser.parse_args()

    input("Press Enter to run curl...")

    os.system('curl %s' % settings.uri)

    input("Press Enter to exit...")

if __name__ == '__main__':
    main()


