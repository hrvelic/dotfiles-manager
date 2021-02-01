# Dotfile Manager

Simple utility scripts form managing links and links to dotfiles in user's home directory. Written in python because that's usually amongst few things available on a freshly installed desktop Linux distribution.

WARNING: Won't work on Windows.

## Scripts

* `dotfile-manager` - manages dotfile links to user's home directory.
* `smartlink` - creates symbolic link only if it's not already linked and backups any existing file of the same name as new link.

## Development
Python script is compiled into a single file with a python shebang for easier distribution. `stickytape` module is used to perform this compilation.

### Prerequisites
To install all the requirements:
`pip install -r requirements.txt`

Requirements can be updated with:
`pip freeze > requirements.txt`

### Assumptions
Project management scripts assume the following convetions:
* `env` directory in project root contains project's virtualenv
* `buld` directory in project root is automatically created and removed when building the project
* `test-temp` directory in project root is automatically recreated whenever a test script is run

### Project Scripts
* `build.sh` - builds manager into a single python script you can put into your dotfiles project
* `test.sh` - run `src/dotfile-manager.py` with given CLI arguments
* `testlink.sh` - run `src/smartlink.py` with given CLI arguments
* `clean.sh` - remove build and test directories and related artifacts

## Running

Run your script of choice with `-h` argument to get help.
