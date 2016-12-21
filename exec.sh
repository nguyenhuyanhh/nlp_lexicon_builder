#!/bin/bash
# Usage ./exec.sh char

python3 operations.py $1
python3 build.py $1
rm -r downloader/download