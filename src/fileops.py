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


def exec_skip_file(operation, is_test=False, verbose=False):
    code, file_path = operation
    validate_operation(code, FileOperation.SKIP)
    print("Skipping", file_path)


def find_backup_name(file_path, backup_index=None):
    if backup_index == None:
        result = file_path + ".backup"
    else:
        result = file_path + ".backup" + str(backup_index)

    return result


def exec_backup_file(operation, is_test=False, verbose=False):
    code, file_path = operation
    validate_operation(code, FileOperation.BACKUP)
    backup_path = find_backup_name(file_path)
    backup_counter = 0
    while (path.lexists(backup_path)):
        backup_counter += 1
        backup_path = find_backup_name(file_path, backup_counter)

    if verbose:
        print("Backing up", file_path, "to", backup_path)
    if not is_test:
        os.rename(file_path, backup_path)


def exec_symlink(operation, is_test=False, verbose=False):
    code, link_path, file_path = operation
    validate_operation(code, FileOperation.SYMLINK)
    if verbose:
        print("Linking", link_path, "->", file_path)
    if not is_test:
        os.symlink(file_path, link_path, target_is_directory=path.isdir(file_path))


def exec_makedir(operation, is_test=False, verbose=False):
    code, dir_name = operation
    validate_operation(code, FileOperation.MKDIR)
    if verbose:
        print("Creating directory", dir_name)
    if not is_test:
        os.makedirs(dir_name)


file_operation_switcher = {
    FileOperation.SKIP: exec_skip_file,
    FileOperation.BACKUP: exec_backup_file,
    FileOperation.SYMLINK: exec_symlink,
    FileOperation.MKDIR: exec_makedir,
}


def execute_file_operation(operation, is_test=False, verbose=False):
    operation_fn = file_operation_switcher.get(operation[0])
    operation_fn(operation, is_test, verbose)


def execute_file_operations(operations, is_test=False, verbose=False):
    for operation in operations:
        execute_file_operation(operation, is_test, verbose)


def skip_file(file_path):
    return (FileOperation.SKIP, file_path)


def backup(file_path):
    return (FileOperation.BACKUP, file_path)


def symlink(link_path, file_path):
    return (FileOperation.SYMLINK, link_path, file_path)


def mkdir(dir_path):
    return (FileOperation.MKDIR, dir_path)
