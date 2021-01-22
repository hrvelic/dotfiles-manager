#!/usr/bin/env bash
source env/bin/activate
rm -rf test-data
mkdir -p test-data
python src/smartlink.py "$@"
