import re
import shlex

from subprocess import Popen, PIPE


def check_index(timestamp, check_only=False):
    if timestamp:
        mm, ss, ff = re.split(r'[:.]', timestamp)
        if int(ss) > 59 or int(ff) > 74:
            raise ValueError('invalid timestamp')
        if not check_only:
            return mm, ss, ff


def check_cue(cue):
    summary = [bool(cue.get('album')),
               bool(cue.get('album performer')),
               bool(cue.get('tracks'))]
    if not all(summary):
        raise ValueError('this cuesheet is not valid')
    if cue['tracks'][0].get('index0') == '00:00:00':
        cue['tracks'][0]['index0'] = None
    if cue['tracks'][0].get('index1') == '00:00:00':
        cue['tracks'][0]['index1'] = None
    for track in cue.get('tracks', list()):
        check_index(track['index0'], check_only=True)
        check_index(track['index1'], check_only=True)
        num = track.get('num')
        if track.get('title') is None:
            raise ValueError(f'bad title for track {num}')
        if track['num'] != '01' and track['index1'] is None:
            raise ValueError(f'bad index for track {num}')
    slash = '/' if cue.get('comment') and cue.get('disc ID') else ''
    cue['commentary'] = f'{cue.get("comment")}{slash}{cue.get("disc ID")}'


def cue_to_seconds(s):
    mm, ss, ff = re.split(r'[:.]', s)
    nn = round(int(ff) / 75, 2)
    return int(mm) * 60 + int(ss) + round(int(ff) / 75, 2)


def ff_to_seconds(s):
    hh, mm, ss, nn = re.split(r'[:.]', s)
    minutes = int(hh) * 60 + int(mm)
    return minutes * 60 + int(ss) + int(nn) / 100


def check_media(media):
    cmd = shlex.split(f'ffmpeg -i {media}')
    with Popen(cmd, stderr=PIPE) as ffmpeg:
        res = ffmpeg.communicate()[1]
    data = grep(
        res.decode('utf-8').split('\n'), 'Duration').strip().split(' ')[1]
    data2 = grep(
        res.decode('utf-8').split('\n'), 'Stream')
    sr = int(data2.split(',')[1].strip().split(' ')[0])
    b = int(get_num(data2.split(',')[-1].strip().strip('s')))
    return ff_to_seconds(data.strip(',')), sr, b


def get_num(s):
    r = ''
    for i in s:
        if i.isnumeric():
            r += i
    return r


def grep(data, s):
    for each in data:
        if s in each:
            return each


def check_couple(cue, gaps):
    length, sr, b = check_media(cue["media"])
    if sr != 44100 or b != 16:
        raise ValueError('the media file is not CDDA')
    last = cue_to_seconds(cue['tracks'][-1]['index1'])
    if length <= last:
        raise ValueError('the media file is too short for this cue')
    for i in range(len(cue['tracks'])):
        print(cue['tracks'][i])
