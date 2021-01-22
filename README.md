# Dotfile Manager

Simple manager script for managing links to dotfiles in user's home directory. Written in python because that's usually amongst few things available on a freshly installed desktop Linux distribution.

WARNING: Won't work on Windows.

## Building
Python script is compiled into a single file with a python shebang for easier distribution. `stickytape` module is used to perform this compilation.

### Assumptions
Scripts assume the following convetions:
* `env` directory contains project's virtualenv
* `buld` directory is automatically created and removed when building the project
* 
NOTE: Scripts expect virtualenv in `env/` directory in project root.

### Scripts
* `build.sh` - builds manager into a single python script you can put into your dotfiles project
* `test.sh` - run `src/dotfile-manager.py` with given CLI arguments
* `clean.sh` - remove build and test directories and related artifacts

## Running

Run dotfile-manager with `-h` argument to get help.
