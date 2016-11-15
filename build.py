import os
import sys
import json
import wave
from decimal import Decimal

import sox

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DOWNLOADER_DIR = os.path.join(CUR_DIR, 'downloader/')
AUDIO_DIR = os.path.join(DOWNLOADER_DIR, 'download/')


def get_duration(path):
    with wave.open(path, 'r') as f:
        return Decimal(f.getnframes()) / f.getframerate()


def mp3_to_wav(path):
    dir, file = os.path.split(path)
    new_file = os.path.splitext(file)[0] + '.wav'
    new_path = os.path.join(dir, new_file)
    if not os.path.exists(new_path):
        tfm = sox.Transformer()
        tfm.convert(samplerate=16000, n_channels=1, bitdepth=16)
        tfm.build(path, new_path)
    return new_path


def main(path):
    start_time = 0
    wav_list = dict()
    file_list = dict()

    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.mp3':
            cur_path = os.path.join(path, file)
            new_path = mp3_to_wav(cur_path)
            file_list[os.path.splitext(file)[0]] = str(get_duration(new_path))
            wav_list[os.path.splitext(file)[0]] = new_path

    with wave.open('a.wav', 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)

    cbm = sox.Combiner()
    for file in sorted(wav_list.keys())[:50]:
        os.rename('a.wav', 'a_temp.wav')
        cbm_list = ['a_temp.wav', wav_list[file]]
        cbm.build(cbm_list, 'a.wav', 'concatenate')

    for file in sorted(file_list.keys()):
        duration = Decimal(file_list[file])
        file_list[file] = str(start_time), str(start_time + duration)
        start_time += duration

    with open('out.json', 'w') as w:
        json.dump(file_list, w, sort_keys=True, indent=4)

if __name__ == '__main__':
    main(sys.argv[1])
