#!/usr/bin/python
# rdb-dircount.py - Count entries in directories
#                   backed up by rdiff-backup
#
# This program expects the output of the command:
#       rdiff-backup list files --changed-since ...
#

import sys
import fileinput

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

def count_actions():
    """Count the actions found in file.
        The first field of each line is the action."""
    global bad_lines
    with fileinput.input() as f:
        for line in f:
            fields = line.rstrip().split(maxsplit=1)
            if fields:
                if len(fields) < 2:
                    bad_lines += 1
                else:
                    actions[fields[0]] = actions.setdefault(fields[0], 0) + 1
                    count_dirs(fields[1])

def display_count_dict(counts, message):
    """Display a dictionary containing the number of occurrences of each key."""
    if len(counts):
        print('')
        print(message)
        print('')
    for tpl in sorted(sorted(counts.items()), key=lambda x: x[1], 
                          reverse=True):
        print(" {:9} {}".format(tpl[1], tpl[0]))

if __name__ == '__main__':
    count_actions()
    display_count_dict(actions, 
                       "There are {} distinct actions.".format(len(actions)))
    display_count_dict(top_dirs, 
            "There are {} top level directories.".format(len(top_dirs)))
    display_count_dict(all_dirs, 
            "There are {} total files and directories.".format(len(all_dirs)))
    if bad_lines:
        print('')
        print("Found", bad_lines, " bad lines.")

