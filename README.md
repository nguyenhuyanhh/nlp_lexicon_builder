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

## Library structure

```
downloader/     # crawler library
build_output/   # builder output
init.sh         # init script
json_ops.py     # json operations
build.py        # builder
```