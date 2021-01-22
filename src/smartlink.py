#!/usr/bin/env python
import argparse
from os import path
from linker import link_if_not_linked
from fileops import execute_file_operations, print_file_operations, has_file_operations

description = "Creates a TARGET link to SOURCE, if TARGET is not already linked to it. If there is an existing file, it creates a backup of it."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("target", metavar="TARGET", help="Link you want to create.")
parser.add_argument("source", metavar="SOURCE", help="File or directory you are linking to.")
parser.add_argument("-t", dest="dryrun", action="store_true",
                    help="Don't execute any actions, only print what you are going to do.")
parser.add_argument("-v", dest="verbose", action="store_true",
                    help="Very verbose output for debugging.")

options = parser.parse_args()
target = path.abspath(options.target)
source = path.abspath(options.source)

file_operations = link_if_not_linked(source, target, verbose=options.verbose)
if has_file_operations(file_operations):
    if options.verbose:
        print("File operations for linking:")
        print_file_operations(file_operations)

    execute_file_operations(file_operations, dryrun=options.dryrun, verbose=options.verbose)
