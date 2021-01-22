#!/usr/bin/env bash
# Find script directory and resolve any links to script
# From: https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
ROOTDIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
# Build manager into a single script
source $ROOTDIR/env/bin/activate
./clean.sh
mkdir -p $ROOTDIR/build

echo "Building dotfile-manager..."
DOTFILE_MANAGER=$ROOTDIR/build/dotfile-manager
stickytape src/dotfile-manager.py \
  --add-python-path $ROOTDIR/src \
  --copy-shebang \
  --output-file $DOTFILE_MANAGER
chmod ug+x $DOTFILE_MANAGER

echo "Building smartlink..."
SMARTLINK=$ROOTDIR/build/smartlink
stickytape src/smartlink.py \
  --add-python-path $ROOTDIR/src \
  --copy-shebang \
  --output-file $SMARTLINK
chmod ug+x $SMARTLINK

echo "Done."
