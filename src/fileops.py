import sys
import os
from os import path
from enum import Enum, auto


class FileOperation(Enum):
    SKIP = auto()
    BACKUP = auto()
    SYMLINK = auto()
    MKDIR = auto()


def validate_operation(code, expected_code):
    if code != expected_code:
        print("Invalid operation! Expected {} but got {}".format(expected_code, code))
        sys.exit(1)


def exec_skip_file(operation, dryrun=False, verbose=False):
    code, file_path = operation
    validate_operation(code, FileOperation.SKIP)
    print("Skipping", file_path)


def find_backup_name(file_path, backup_index=None):
    if backup_index == None:
        result = file_path + ".backup"
    else:
        result = file_path + ".backup" + str(backup_index)

    return result


def exec_backup_file(operation, dryrun=False, verbose=False):
    code, file_path = operation
    validate_operation(code, FileOperation.BACKUP)
    backup_path = find_backup_name(file_path)
    backup_counter = 0
    while (path.lexists(backup_path)):
        backup_counter += 1
        backup_path = find_backup_name(file_path, backup_counter)

    if verbose:
        print("Backing up", file_path, "to", backup_path)
    if not dryrun:
        os.rename(file_path, backup_path)


def exec_symlink(operation, dryrun=False, verbose=False):
    code, source, link = operation
    validate_operation(code, FileOperation.SYMLINK)
    if verbose:
        print("Linking '{}' -> '{}'.".format(link, source))
    if not dryrun:
        # apparently, relative links work off current working directory
        os.chdir(path.dirname(link))
        os.symlink(source, link)


def exec_makedir(operation, dryrun=False, verbose=False):
    code, dir_name = operation
    validate_operation(code, FileOperation.MKDIR)
    if verbose:
        print("Creating directory", dir_name)
    if not dryrun:
        os.makedirs(dir_name)


file_operation_switcher = {
    FileOperation.SKIP: exec_skip_file,
    FileOperation.BACKUP: exec_backup_file,
    FileOperation.SYMLINK: exec_symlink,
    FileOperation.MKDIR: exec_makedir,
}


def execute_file_operation(operation, dryrun=False, verbose=False):
    operation_fn = file_operation_switcher.get(operation[0])
    operation_fn(operation, dryrun, verbose)


def execute_file_operations(operations, dryrun=False, verbose=False):
    for operation in operations:
        execute_file_operation(operation, dryrun, verbose)

def print_file_operations(operations):
    for operation in operations:
        print("Operation: [" + str(operation) + "].")

def has_file_operations(operations):
    return len(operations) > 0

def skip_file(file_path):
    return (FileOperation.SKIP, file_path)


def backup(file_path):
    return (FileOperation.BACKUP, file_path)


def symlink(source_path, link_path, absolute=False):
    if absolute:
        source_path = path.abspath(source_path)
        link_path = path.abspath(link_path)
    return (FileOperation.SYMLINK, source_path, link_path)


def mkdir(dir_path):
    return (FileOperation.MKDIR, dir_path)
