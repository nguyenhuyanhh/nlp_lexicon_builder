import os
import sys
import json
import wave
from decimal import Decimal
from time import time

import sox
from slugify import slugify

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DOWNLOADER_DIR = os.path.join(CUR_DIR, 'downloader/')
AUDIO_DIR = os.path.join(DOWNLOADER_DIR, 'download/')
OUTPUT_DIR = os.path.join(CUR_DIR, 'build_output/')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
PADDING = 0.5


def get_duration(path):
    """Helper function to get duration of wav file."""
    with wave.open(path, 'r') as f:
        return Decimal(f.getnframes()) / f.getframerate()


def mp3_to_wav(path):
    """Helper function to convert mp3 to wav using sox."""
    dir, file = os.path.split(path)
    new_file = slugify(os.path.splitext(file)[0]) + '.wav'
    new_path = os.path.join(dir, new_file)
    if not os.path.exists(new_path):
        tfm = sox.Transformer()
        tfm.convert(samplerate=16000, n_channels=1, bitdepth=16)
        tfm.pad(end_duration=PADDING)
        tfm.build(path, new_path)
    return new_path


def main(path, char):
    """
    Build the lexicon wav file of all words starting with char.
    All raw mp3 files are under path.
    """
    start_time = 0
    wav_list = dict()
    file_list = dict()
    wav_out = os.path.join(OUTPUT_DIR, '{}.wav'.format(char))
    wav_temp = os.path.join(OUTPUT_DIR, '{}_temp.wav'.format(char))
    json_out = os.path.join(OUTPUT_DIR, '{}.json'.format(char))

    # populate file list and wav list
    for file in os.listdir(path):
        if (os.path.splitext(file)[0][0] == char and os.path.splitext(file)[1] == '.mp3'):
            cur_path = os.path.join(path, file)
            new_path = mp3_to_wav(cur_path)
            file_list[os.path.splitext(file)[0]] = str(
                get_duration(new_path) - Decimal(PADDING))
            wav_list[os.path.splitext(file)[0]] = new_path

    # create empty output file
    with wave.open(wav_out, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)

    # combine, a few files at once
    sorted_keys = sorted(wav_list.keys())
    files_per_round = 50
    no_rounds = int(len(sorted_keys) / files_per_round)

    for round in range(no_rounds - 1):
        os.rename(wav_out, wav_temp)
        cbm_wav_list = [wav_list[sorted_keys[i]] for i in range(
            round * files_per_round, (round + 1) * files_per_round)]
        cbm_list = [wav_temp] + cbm_wav_list
        cbm = sox.Combiner()
        cbm.build(cbm_list, wav_out, 'concatenate')
    os.rename(wav_out, wav_temp)
    cbm_wav_list = [wav_list[sorted_keys[i]] for i in range(
        (no_rounds - 1) * files_per_round, len(sorted_keys))]
    cbm_list = [wav_temp] + cbm_wav_list
    cbm = sox.Combiner()
    cbm.build(cbm_list, wav_out, 'concatenate')
    os.remove(wav_temp)

    # build json
    for file in sorted(file_list.keys()):
        duration = Decimal(file_list[file])
        file_list[file] = str(start_time), str(start_time + duration)
        start_time += (duration + Decimal(PADDING))
    with open(json_out, 'w') as w:
        json.dump(file_list, w, sort_keys=True, indent=4)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
