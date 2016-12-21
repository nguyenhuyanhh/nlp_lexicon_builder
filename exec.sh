#!/bin/bash
# Usage ./exec.sh char

python3 operations.py $1

if [ $? -eq 0 ]
then
    python3 build.py $1
else
    exit 1
fi