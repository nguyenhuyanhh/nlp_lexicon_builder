import json
import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DOWNLOADER_DIR = os.path.join(CUR_DIR, 'downloader/')


def clean_json():
    pattern_fail = 'http://www.oxforddictionaries.com/'
    with open(os.path.join(DOWNLOADER_DIR, 'ultimate.json'), 'r') as f:
        ultimate_list = json.load(f)
    clean_list = dict()
    for word, links in ultimate_list.items():
        for link in links:
            if link.find(pattern_fail) < 0:
                clean_list[word] = link
                break
    with open(os.path.join(DOWNLOADER_DIR, 'clean.json'), 'w') as w:
        json.dump(clean_list, w, sort_keys=True, indent=4)


def split_json():
    pass

if __name__ == '__main__':
    clean_json()
