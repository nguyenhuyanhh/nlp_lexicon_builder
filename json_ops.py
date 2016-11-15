import json
import os
import shutil

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DOWNLOADER_DIR = os.path.join(CUR_DIR, 'downloader/')


def clean_json():
    fails = ['www.oxforddictionaries.com', 'www.onelook.com']
    with open(os.path.join(DOWNLOADER_DIR, 'ultimate.json'), 'r') as f:
        ultimate_list = json.load(f)
    clean_list = dict()
    for word, links in ultimate_list.items():
        for link in links:
            if (link.find(fails[0]) < 0 and link.find(fails[1]) < 0):
                clean_list[word] = link
                break
    with open(os.path.join(DOWNLOADER_DIR, 'clean.json'), 'w') as w:
        json.dump(clean_list, w, sort_keys=True, indent=4)


def split_json(char):
    with open(os.path.join(DOWNLOADER_DIR, 'clean.json'), 'r') as f:
        clean_list = json.load(f)
    split_list = dict()
    for word, link in clean_list.items():
        if word[0] == char:
            split_list[word] = link
    with open(os.path.join(DOWNLOADER_DIR, 'clean_{}.json'.format(char)), 'w') as w:
        json.dump(split_list, w, sort_keys=True, indent=4)


def change_data_json(path):
    os.remove(os.path.join(DOWNLOADER_DIR, 'data.json'))
    shutil.copy(path, os.path.join(DOWNLOADER_DIR, 'data.json'))

if __name__ == '__main__':
    clean_json()
    split_json('a')
    change_data_json(os.path.join(DOWNLOADER_DIR, 'clean_a.json'))
