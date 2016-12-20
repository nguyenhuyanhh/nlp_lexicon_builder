"""Module for JSON operations."""

import json
import logging
import os
import shutil
import sys

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DOWNLOADER_DIR = os.path.join(CUR_DIR, 'downloader/')
DATA_JSON = os.path.join(DOWNLOADER_DIR, 'data.json')
DATA_BAK = os.path.join(DOWNLOADER_DIR, 'data.json.bak')
ULTIMATE_JSON = os.path.join(DOWNLOADER_DIR, 'ultimate.json')
ULTIMATE_BAK = os.path.join(DOWNLOADER_DIR, 'ultimate.json.bak')
CLEAN_JSON = os.path.join(DOWNLOADER_DIR, 'clean.json')

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def backup():
    """Backup data.json and ultimate.json."""
    shutil.copy(DATA_JSON, DATA_BAK)
    shutil.copy(ULTIMATE_JSON, ULTIMATE_BAK)
    LOG.info('Backup completed.')


def restore():
    """Restore data.json and ultimate.json."""
    shutil.copy(DATA_BAK, DATA_JSON)
    shutil.copy(ULTIMATE_JSON, ULTIMATE_BAK)
    LOG.info('Restore completed.')


def clean():
    """Get a file similar to data.json, without the failed urls."""
    fails = ['www.oxforddictionaries.com', 'www.onelook.com']
    with open(ULTIMATE_JSON, 'r') as file_:
        ultimate_list = json.load(file_)
    clean_list = dict()
    for word, links in ultimate_list.items():
        for link in links:
            if link.find(fails[0]) < 0 and link.find(fails[1]) < 0:
                clean_list[word] = link
                break
    with open(CLEAN_JSON, 'w') as file_out:
        json.dump(clean_list, file_out, sort_keys=True, indent=4)
    LOG.info('clean.json written.')


def split(char):
    """Get a file similar to data.json, only for words starting with char."""
    with open(CLEAN_JSON, 'r') as file_:
        clean_list = json.load(file_)
    split_list = dict()
    for word, link in clean_list.items():
        if word[0] == char:
            split_list[word] = link
    split_json = os.path.join(DOWNLOADER_DIR, 'clean_{}.json'.format(char))
    with open(split_json, 'w') as file_out:
        json.dump(split_list, file_out, sort_keys=True, indent=4)
    LOG.info('Obtained json for %s.', char)
    return split_json


def switch(path):
    """Replace data.json with another similar json file."""
    os.remove(DATA_JSON)
    shutil.copy(path, DATA_JSON)
    LOG.info('Switch completed.')


def operations(char):
    """Perform all operations on words starting with char."""
    if not (os.path.exists(DATA_BAK) or os.path.exists(ULTIMATE_BAK)):
        backup()
    if not os.path.exists(CLEAN_JSON):
        clean()
    split_json = split(char)
    switch(split_json)
    LOG.info('Operations completed for %s.', char)


if __name__ == '__main__':
    operations(sys.argv[1])
