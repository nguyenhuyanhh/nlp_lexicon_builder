#!/bin/bash
# Usage ./exec.sh char

python3 json_ops.py $1
cd downloader/
python3 download_all_mp3.py
cd ..
python3 build.py $1