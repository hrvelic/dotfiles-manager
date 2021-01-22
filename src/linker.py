import os
from os import path
from fileops import backup, symlink, mkdir

def abs_path(relative_path, root=os.getcwd()):
    return path.normpath(path.join(root, relative_path))

def backup_if_exists(file_path, verbose):
    if path.lexists(file_path):
        if verbose:
            print("Backing up existing file:", file_path)
        return [backup(file_path)]

    if verbose:
        print("Skipping backup, no file:", file_path)
    return []


def link_if_not_linked(target_path, link_path, verbose=False):
    target_path = abs_path(target_path)
    link_path = abs_path(link_path)
    if verbose:
        print("Check if \"{}\" links to \"{}\"".format(link_path, target_path))


    if path.exists(link_path) and path.samefile(link_path, target_path):
        # Valid link already exists
        if verbose:
            print("  Already linked. Skipping.")
        # return [skip_file(link_path)]
        return []

    link_target_path = relative_path_to(target_path, path.dirname(link_path))
    if verbose:
        print("  Not linked. Linking to", link_target_path)

    result = []
    result += backup_if_exists(link_path, verbose)
    result.append(symlink(link_target_path, link_path))
    return result


home_directory = path.expanduser("~")

def home_dir():
    return home_directory


def relative_path_to(directory, root_dir):
    # result = path.relpath(directory, root_dir)
    # if result.startswith("."):
    #     return result
    # return path.join(".", result)
    return path.relpath(directory, root_dir)


def link_to_dotfiles_dir(dotfiles_directory, dotfiles_dir_link, verbose=False):
    print("Checking link to dotfiles directory...")
    return link_if_not_linked(dotfiles_directory, dotfiles_dir_link, verbose)

def link_files(dotfiles_directory, destination_directory, verbose=False):
    # def recursively_link_files(link_directory, file_directory, shortcut_directory, verbose):
    file_operations = []
    for filename in os.listdir(dotfiles_directory):
        dotfile_path = path.join(dotfiles_directory, filename)
        # skip files and directories ending with .disabled
        if filename.endswith(".disabled"):
            if verbose:
                print("Skipping disabled file:", dotfile_path)
            continue

        link_path = path.join(destination_directory, filename)
        if path.isdir(dotfile_path):
            # Recurse into directories, and link files in them
            subdir_operations = link_files(dotfile_path, link_path, verbose)
            if not path.isdir(link_path) and len(subdir_operations) > 0:
                # Only create directories if there were files to link in them
                file_operations += backup_if_exists(link_path, verbose)
                file_operations.append(mkdir(link_path))
            file_operations += subdir_operations
        else:
            file_operations += link_if_not_linked(dotfile_path, link_path, verbose)

    return file_operations

