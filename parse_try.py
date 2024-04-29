#!/usr/bin/python
# Try some things with parsers
#

import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--by-count', '-c', action='store_true', 
                   help='sort by descending count, then by name (the default)')
group.add_argument('--by-name', '-n', action='store_true',
                   help='sort entries by name')

print(parser.parse_args())
print(parser.parse_args(['--by-count']))
print(parser.parse_args(['--by-name']))

