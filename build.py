"""Module for build operations."""

import os
import sys
import json
import logging
import wave
from decimal import Decimal

import sox
from slugify import slugify

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DOWNLOADER_DIR = os.path.join(CUR_DIR, 'downloader/')
AUDIO_DIR = os.path.join(DOWNLOADER_DIR, 'download/')
OUTPUT_DIR = os.path.join(CUR_DIR, 'build_output/')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
PADDING = 0.5

logging.basicConfig(level=logging.INFO)
logging.getLogger().disabled = True
LOG = logging.getLogger(__name__)


def slugify_name(path_):
    """Helper function to slugify a file name."""
    dir_, file_ = os.path.split(path_)
    name, ext = os.path.splitext(file_)
    new_path = os.path.join(dir_, slugify(name) + ext)
    if not path_ == new_path:
        os.rename(path_, new_path)
    return new_path


def mp3_to_wav(path_):
    """Helper function to convert mp3 to wav with padding using sox."""
    dir_, file_ = os.path.split(path_)
    new_file = os.path.splitext(file_)[0] + '.wav'
    new_path = os.path.join(dir_, new_file)
    if not os.path.exists(new_path):
        tfm = sox.Transformer()
        tfm.convert(samplerate=16000, n_channels=1, bitdepth=16)
        tfm.pad(end_duration=PADDING)
        tfm.build(path_, new_path)
    return new_path


def get_duration(path):
    """Helper function to get duration of wav file."""
    with wave.open(path, 'r') as file_:
        return Decimal(file_.getnframes()) / file_.getframerate()


def main(char):
    """
    Build the lexicon wav file of all words starting with char.
    Assume all raw mp3 files are under ./downloader/download.
    """
    start_time = 0
    wav_list = dict()
    file_list = dict()
    wav_out = os.path.join(OUTPUT_DIR, '{}.wav'.format(char))
    wav_temp = os.path.join(OUTPUT_DIR, '{}_temp.wav'.format(char))
    json_out = os.path.join(OUTPUT_DIR, '{}.json'.format(char))

    # populate file list and wav list
    # slugify file names as an intermediate to prevent errors
    for file_ in os.listdir(AUDIO_DIR):
        name, ext = os.path.splitext(file_)
        if name[0] == char and ext == '.mp3':
            cur_path = os.path.join(AUDIO_DIR, file_)
            temp_path = slugify_name(cur_path)
            new_path = mp3_to_wav(temp_path)
            if not temp_path == cur_path:
                os.rename(temp_path, cur_path)
            file_list[name] = str(
                get_duration(new_path) - Decimal(PADDING))
            wav_list[name] = new_path
            LOG.info('Processed %s', name)

    # create empty output file
    with wave.open(wav_out, 'w') as file_out:
        file_out.setnchannels(1)
        file_out.setsampwidth(2)
        file_out.setframerate(16000)

    # combine, a few files at once
    sorted_keys = sorted(wav_list.keys())
    files_per_round = 100
    no_rounds = int(len(sorted_keys) / files_per_round)
    completed = 0

    for round_ in range(no_rounds - 1):
        os.rename(wav_out, wav_temp)
        cbm_wav_list = [wav_list[sorted_keys[i]] for i in range(
            round_ * files_per_round, (round_ + 1) * files_per_round)]
        cbm_list = [wav_temp] + cbm_wav_list
        cbm = sox.Combiner()
        cbm.build(cbm_list, wav_out, 'concatenate')
        completed += len(cbm_wav_list)
        LOG.info('Completed %s files.', completed)
    os.rename(wav_out, wav_temp)
    cbm_wav_list = [wav_list[sorted_keys[i]] for i in range(
        (no_rounds - 1) * files_per_round, len(sorted_keys))]
    cbm_list = [wav_temp] + cbm_wav_list
    cbm = sox.Combiner()
    cbm.build(cbm_list, wav_out, 'concatenate')
    completed += len(cbm_wav_list)
    os.remove(wav_temp)
    LOG.info('Completed %s files.', completed)
    LOG.info('Finish building wav file for %s.', char)

    # build json
    for file_ in sorted(file_list.keys()):
        duration = Decimal(file_list[file_])
        file_list[file_] = str(start_time), str(start_time + duration)
        start_time += (duration + Decimal(PADDING))
    with open(json_out, 'w') as file_out:
        json.dump(file_list, file_out, sort_keys=True, indent=4)
    LOG.info('JSON written for %s.', char)

if __name__ == '__main__':
    main(sys.argv[1])
