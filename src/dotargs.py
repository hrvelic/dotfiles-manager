import argparse

description = "Link files into user's home directory. Existing files are backed up and already valid links are ignored."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("path", help="Path to directory to link to")
parser.add_argument("--test", dest="test", action="store_const", const=True, default=False,
                    help="Don't execute any actions, only print what you are going to do.")
parser.add_argument("--verbose", dest="verbose", action="store_const", const=True, default=False,
                    help="Very verbose output for debugging")

def parse_arguments():
    return parser.parse_args()
