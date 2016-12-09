# nlp_lexicon_builder

This library combines pronunciations of single words into big files and indexes, which allows easy storage and retrieval for lexicon analysis. The audio files have already been [crawled](https://github.com/nathanielove/English-words-pronunciation-mp3-audio-download) from various online sources.

## Requirements

1. Linux
1. Python 3

This library is developed using Python 3.5.2 on Lubuntu 16.04.1 LTS.

## Setup

1. Clone the project
1. Install SoX with mp3 support: `$ sudo apt-get install sox libsox-fmt-all`
1. Install Python dependencies: `$ sudo pip3 install -r requirements.txt`
1. Run the init script: `$ ./init.sh`
1. Run the exec script, takes any letter as argument to build lexicon for that letter: `$ ./exec.sh char`

## Library structure

```
downloader/             # crawler library
    download/           # raw mp3 files and converted wav files
    ultimate.json       # source json
    clean.json          # source json after cleanup
    clean_a.json        # clean json for a
    clean_b.json
    ...
    data.json           # currently processed json
    download_all_mp3.py # downloader script
build_output/           # builder output
    a.wav               # wav file
    a.json              # json file
    b.wav
    b.json
    ...
init.sh                 # init script
json_ops.py             # json operations
build.py                # builder
exec.sh                 # exec script
```