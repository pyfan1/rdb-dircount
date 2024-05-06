#!/usr/bin/python
# Try some things with parsers
#

import argparse
import fileinput

CHECK_PARSE = False

parser = argparse.ArgumentParser(description='This is what the program does.')
group = parser.add_mutually_exclusive_group()
group.add_argument('--by-count', '-c', action='store_true', 
                   help='sort by descending count, then by name (the default)')
group.add_argument('--by-name', '-n', action='store_true',
                   help='sort entries by name')

parse_namespace, remaining_args = parser.parse_known_args()
print(parse_namespace)
if CHECK_PARSE:
    print(parser.parse_args(['--by-count']))
    print(parser.parse_args(['--by-name']))
else:
    with fileinput.input(remaining_args) as f:
        for line in f:
            if fileinput.isfirstline():
                print('Filename: {}  fileno: {}.'.format(fileinput.filename(), fileinput.fileno() ) )
                print('    Line: {}  Is stdin: {}.'.format(fileinput.lineno(), fileinput.isstdin() ) )

