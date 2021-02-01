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
$ROOTDIR/clean.sh
mkdir -p $ROOTDIR/build

function build_script {
	stickytape $1 \
		--add-python-path $ROOTDIR/src \
		--copy-shebang \
		--output-file $2
	chmod ug+x $2
}

echo "Building dotfile-manager..."
build_script "src/dotfile-manager.py" "$ROOTDIR/build/dotfile-manager"

echo "Building smartlink..."
build_script "src/smartlink.py" "$ROOTDIR/build/smartlink"

echo "Done."
