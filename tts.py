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
logging.getLogger().disabled = True
LOG = logging.getLogger(__name__)


class Tts():
    """
    Class for TTS operations using a lexicon folder.
    Syntax: Tts(path_)
    """

    def __init__(self, path_):
        """Load lexicon information from a folder."""
        self.lexpath = os.path.abspath(path_)
        lexicon = dict()
        for file_ in os.listdir(self.lexpath):
            if os.path.splitext(file_)[1] == '.json':
                index = os.path.splitext(file_)[0]
                with open(os.path.join(self.lexpath, file_), 'r') as lookup_:
                    lookup = json.load(lookup_)
                lexicon[index] = lookup
        self.lexicon = lexicon
        LOG.info('Loaded %s.', path_)

    def pronounce(self, word):
        """Extract pronunciation of a word to wav."""
        index = word[0]
        lookup = self.lexicon[index]
        try:
            start_time = Decimal(lookup[word][0])
            end_time = Decimal(lookup[word][1])
            wav_file = os.path.join(self.lexpath, '{}.wav'.format(index))
            out_file = os.path.join(TTS_DIR, '{}.wav'.format(word))
            tfm = sox.Transformer()
            tfm.trim(start_time, end_time)
            tfm.pad(end_duration=0.1)
            tfm.build(wav_file, out_file)
            LOG.info('Processed %s', word)
            return out_file
        except KeyError:
            LOG.info('Not found: %s', word)
            return None


if __name__ == '__main__':
    TTS = Tts(os.path.join(CUR_DIR, 'build_output/'))
    TTS.pronounce('apple')
    TTS.pronounce('gaygisu')
