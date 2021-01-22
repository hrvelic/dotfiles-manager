#!/usr/bin/env python
import argparse
import os
from os import path
from linker import link_to_dotfiles_dir, link_files, home_dir
from fileops import execute_file_operations, print_file_operations, has_file_operations

description = "Link files into user's home directory. Existing files are backed up and already valid links are ignored."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("dotfiles_directory", metavar="DOTFILES_DIRECTORY",
                    help="Path to directory to link to.")
parser.add_argument("-p", dest="link_directory", default=home_dir(),
                    help="Directory to put links into. Default: user's home directory ({}).".format(home_dir()))
parser.add_argument("-l", dest="link_name", default=".dotfiles",
                    help="Name of the link to dotfiles directory. Default: \".dotfiles\".")
parser.add_argument("-1", dest="run_files", action="store_false",
                    help="Only create link to dotfiles directory.")
parser.add_argument("-t", dest="dryrun", action="store_true",
                    help="Don't execute any actions, only print what you are going to do. WARNING: if there isn't already a link to dotfiles directory file operations might not be correct.")
parser.add_argument("-v", dest="verbose", action="store_true",
                    help="Very verbose output for debugging.")


options = parser.parse_args()
dotfiles_directory = path.normpath(path.realpath(options.dotfiles_directory))
link_directory = path.normpath(path.realpath(path.expanduser(options.link_directory)))
link_path = path.join(link_directory, options.link_name)
task_count = 0



# First create link to dotfiles. Otherwise if dotfiles project got moved, it would try to relink all the files.
dir_operations = link_to_dotfiles_dir(dotfiles_directory, link_path, options.verbose)
if has_file_operations(dir_operations):
    task_count += 1
    if options.verbose:
        print("File operations for directory link to dotfiles directory:")
        print_file_operations(dir_operations)

    execute_file_operations(dir_operations, options.dryrun, options.verbose)

# Link individual dotfiles
if options.run_files:
    # Link dot files via dotfiles directory link
    file_operations = link_files(link_path, link_directory, options.verbose)
    if has_file_operations(file_operations):
        task_count += 1
        if options.verbose:
            if options.dryrun:
                print("WARNING: if link to dotfiles directory does not exist on a dry run link operations might be incorrect.")
            print("File operations to link individual dot files:")
            print_file_operations(file_operations)

        execute_file_operations(file_operations, options.dryrun, options.verbose)

if task_count == 0:
    print("Nothing to do: everything up to date. Exiting.")
