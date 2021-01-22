import os
from os import path
from fileops import backup, symlink, mkdir


def backup_if_exists(file_path, verbose):
    result = []
    if path.lexists(file_path):
        result.append(backup(file_path))
    else:
        if verbose:
            print("No backup, doesn't exist:", file_path)

    return result


def link_if_not_linked(link_path, target_path, verbose):
    if verbose:
        print("Link check input", link_path, target_path)

    norm_target_path = path.abspath(path.expanduser(target_path))
    if verbose:
        print("Link check normalized", link_path, norm_target_path)

    if path.exists(link_path) and path.samefile(link_path, norm_target_path):
        # Valid link already exists
        if verbose:
            print("Already linked", link_path)

        # return [skip_file(link_path)]
        return []

    if verbose:
        print("Requires linking", link_path)
    result = []
    result += backup_if_exists(link_path, verbose)
    result.append(symlink(link_path, norm_target_path))
    return result


home_directory = path.expanduser("~")

def home_rel_path(target_path):
    return path.join("~", path.relpath(target_path, home_directory))


def recursively_link_files(link_directory, file_directory, shortcut_directory, verbose):
    file_operations = []
    for filename in os.listdir(file_directory):
        # skip files and directories ending with .disabled
        if filename.endswith(".disabled"):
            continue
        link_file_path = path.join(link_directory, filename)
        file_path = path.join(file_directory, filename)
        shortcut_path = path.join(shortcut_directory, filename)
        if path.isdir(file_path):
            # Recurse into directories, and link files in them
            subdir_operations = recursively_link_files(
                link_file_path, file_path, shortcut_path, verbose)
            if not path.isdir(link_file_path) and len(subdir_operations) > 0:
                # Only create directories if there were files to link in them
                file_operations += backup_if_exists(link_file_path, verbose)
                file_operations.append(mkdir(link_file_path))

            file_operations += subdir_operations
        else:
            file_operations += link_if_not_linked(link_file_path, shortcut_path, verbose)

    return file_operations


def install_links_to_home(target_directory, dotfiles_link_name, verbose=False):
    print("Preparing...")
    dotfiles_dir_link = path.join(home_directory, dotfiles_link_name)
    file_operations = []
    if verbose:
        print("home directory", home_directory)
        print("dotfile dir link", dotfiles_dir_link)
        print("target directory", target_directory)

    # Link .dotfiles in user's home
    file_operations += link_if_not_linked(
        dotfiles_dir_link,
        home_rel_path(target_directory),
        verbose
    )

    # link dot files from dotfiles/home into user's home via .dotfiles link
    file_operations += recursively_link_files(
        home_directory,
        target_directory,
        home_rel_path(dotfiles_dir_link),
        verbose
    )
    return file_operations

