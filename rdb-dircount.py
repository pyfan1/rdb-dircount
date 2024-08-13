#!/usr/bin/python
# rdb-dircount.py - Count entries in directories
#                   backed up by rdiff-backup
#
# This program expects the output of the command:
#       rdiff-backup list files --changed-since ...
#
# Copyright (C) 2024  David Webster
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    You can reach the author by email at the following address:
#    pyfan1 AT gmail DOT com

import fileinput
import argparse

actions = {}
bad_lines = 0
top_dirs = {}
all_dirs = {}

def count_subdirs(components):
    """Count each component of the path for one subdirectory."""
    parent = ''
    for comp in components:
        if parent:
            parent = parent + '/' + comp
        else:
            parent = comp
        all_dirs[parent] = all_dirs.setdefault(parent, 0) + 1

def count_dirs(path):
    """Split the path into separate directories and count them."""
    folders = path.split(sep='/')
    if len(folders) > 0:
        top_dirs[folders[0]] = top_dirs.setdefault(folders[0], 0) + 1
        count_subdirs(folders)

def count_actions(file_list):
    """Count the actions found in file.
        The first field of each line is the action."""
    global bad_lines
    with fileinput.input(file_list) as f:
        for line in f:
            fields = line.rstrip().split(maxsplit=1)
            if fields:
                if len(fields) < 2:
                    bad_lines += 1
                else:
                    actions[fields[0]] = actions.setdefault(fields[0], 0) + 1
                    count_dirs(fields[1])

def display_count_dict(counts, message, options):
    """Display a dictionary containing the number of occurrences of each key."""
    if len(counts):
        print('')
        print(message)
        print('')
    lineout = lambda first, second: print(" {:9} {}".format(first, second))
    if options.by_name and not options.by_count:    # Which sort order?
        # Sorting by name - since dictionary keys are unique
        # there's no need to do more than one sort
        for tpl in sorted(counts.items()):
            lineout(tpl[1], tpl[0])
    else:   # Sorting by count
        # We rely on the fact that Python uses a stable sort algorithm.
        # The inner sort is on the key and the outer is on the value
        # so the entries appear sorted first by count and then by name
        # within each count.
        for tpl in sorted(sorted(counts.items()), key=lambda x: x[1], 
                          reverse=True):
            lineout(tpl[1], tpl[0])

def parse_command():
    """Analyze command line and return opions and file names."""
    parser = argparse.ArgumentParser(
            description='Count directories and files backed up by rdiff-backup.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--by-count', '-c', action='store_true', 
                   help='sort by descending count, then by name (the default)')
    group.add_argument('--by-name', '-n', action='store_true',
                   help='sort entries by name')
    return parser.parse_known_args()

if __name__ == '__main__':
    options, file_list = parse_command()
    count_actions(file_list)
    display_count_dict(actions, 
             "There are {} distinct actions.".format(len(actions)),
             options)
    display_count_dict(top_dirs, 
            "There are {} top level directories.".format(len(top_dirs)),
            options)
    display_count_dict(all_dirs, 
            "There are {} total files and directories.".format(len(all_dirs)),
            options)
    if bad_lines:
        print('')
        print("Found", bad_lines, " bad lines.")

