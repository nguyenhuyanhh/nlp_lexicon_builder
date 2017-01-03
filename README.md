# nlp_lexicon_builder

This library combines pronunciations of single words into big files and indexes, which allows easy storage and retrieval for lexicon analysis. The audio files have already been [crawled](https://github.com/nathanielove/English-words-pronunciation-mp3-audio-download) from various online sources.

The lexicon is then used for text-to-speech operations.

## Requirements

1. Linux
1. Python 3

This library is developed using Python 3.5.2 on Lubuntu 16.04.1 LTS.

## Setup (Lexicon builder)

1. Clone the project
1. Install SoX with mp3 support: `$ sudo apt-get install sox libsox-fmt-all`
1. Install Python dependencies: `$ sudo pip3 install -r requirements.txt`
1. Run the init script: `$ ./init.sh`
1. Run the exec script, takes any letter as argument to build lexicon for that letter: `$ ./exec.sh char`

## Text-to-speech

1. Make sure all wav and json files are inside `/build_output`
1. Input text into `/tts/input.txt`
1. Run the TTS script: `$ python3 tts.py`

## Library structure

```
downloader/             # crawler library
    download/           # raw mp3 files and converted wav files
    ultimate.json       # source json
    clean.json          # source json after cleanup
    data.json           # currently processed json
    download_all_mp3.py # downloader script
build_output/           # builder output
    a.wav               # wav file
    a.json              # json file
    b.wav
    b.json
    ...
tts/                    
    input.txt           # tts input file
    result.wav          # tts output file
init.sh                 # init script
operations.py           # json and downloader operations
build.py                # builder
exec.sh                 # exec script
tts.py                  # text-to-speech operations
```