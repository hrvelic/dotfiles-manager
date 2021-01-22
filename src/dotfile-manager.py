#!/usr/bin/env python

import sys
from os import path
from dotargs import parse_arguments
from linker import install_links_to_home
from fileops import execute_file_operations


def exit_with_message(message):
    print(message)
    sys.exit(1)


options = parse_arguments()
source_path = path.normpath(path.realpath(options.path))
is_dryrun = options.test
is_verbose = options.verbose


file_operations = install_links_to_home(source_path, ".dotfiles", is_verbose)

if len(file_operations) == 0:
    exit_with_message("Nothing to do: everything up to date. Exiting.")

if is_verbose:
    print("Prepared file operations:")
    for operation in file_operations:
        print("Operation: [" + str(operation) + "].")

print("Executing file operations...")
execute_file_operations(file_operations, is_dryrun, True)
