#!/usr/bin/env bash
source env/bin/activate
rm -rf test-temp
mkdir -p test-temp
python src/dotfile-manager.py "$@"
