"""Module for text-to-speech operations."""

import os
import json
import logging
from decimal import Decimal

import sox

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TTS_DIR = os.path.join(CUR_DIR, 'tts/')
if not os.path.exists(TTS_DIR):
    os.makedirs(TTS_DIR)

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def load_folder(path_):
    """Load lexicon information from a folder."""
    lexicon = dict()
    for file_ in os.listdir(path_):
        if os.path.splitext(file_)[1] == '.json':
            index = os.path.splitext(file_)[0]
            with open(os.path.join(path_, file_), 'r') as lookup_:
                lookup = json.load(lookup_)
            lexicon[index] = lookup
    with open(os.path.join(TTS_DIR, 'lexicon.json'), 'w') as file_out:
        json.dump(lexicon, file_out, sort_keys=True, indent=4)
    LOG.info('Loaded %s.', path_)
    return lexicon

if __name__ == '__main__':
    load_folder(os.path.join(CUR_DIR, 'build_output/'))
