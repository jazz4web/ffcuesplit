import importlib.util
import os
import re

from .system import detect_f_type


def make_couple(filename, res):
    medias = ('.wv', '.flac', '.ape')
    cues = ('.cue', '.cue~')
    if not os.path.exists(filename):
        raise FileNotFoundError(f'"{filename}" does not exist')
    source = os.path.realpath(filename)
    hd = os.path.dirname(source)
    name, ext = os.path.splitext(os.path.basename(source))
    if ext in cues:
        for each in medias:
            m = os.path.join(hd, name + each)
            if os.path.exists(m):
                res['media'] = m
                res['cue'] = source
                break
        else:
            raise FileNotFoundError('cannot find an appropriate media file')
    elif ext in medias:
        for each in cues:
            c = os.path.join(hd, name + each)
            if os.path.exists(c):
                res['cue'] = c
                res['media'] = source
                break
        else:
            raise FileNotFoundError('cannot find an appropriate cue file')


def read_file(name):
    if importlib.util.find_spec('chardet') is None:
        raise OSError('python3 module `chardet` is not installed')
    from chardet import detect
    t = detect_f_type(name)
    if t != 'text/plain':
        raise ValueError('bad cue')
    try:
        with open(name, 'rb') as f:
            enc = detect(f.read())['encoding']
            f.seek(0)
            return [line.decode(enc).rstrip() for line in f]
    except(OSError, ValueError):
        return None


def get_value(content, expression, index=False):
    pattern = re.compile(expression)
    for line in content:
        box = pattern.match(line)
        if box:
            if index:
                return box.group(1)
            return box.group(1).strip('"')


def get_tracks(content):
    res = list()
    i = 0
    pattern = re.compile(r'^ +TRACK +(\d+) +(.+)')
    for step, item in enumerate(content):
        box = pattern.match(item)
        if box:
            track = dict()
            track['num'] = box.group(1)
            track['this'] = step
            if i:
                res[i - 1]['next'] = step
            res.append(track)
            i += 1
    print(f'there are {len(res)} tracks')
    return res


def get_tracks_meta(content, tracks, performer):
    title = r'^ +TITLE +(.+)'
    perf = r'^ +PERORMER +(.+)'
    index0 = r'^ +INDEX 00 +(\d{2}:\d{2}:\d{2})'
    index1 = r'^ +INDEX 01 +(\d{2}:\d{2}:\d{2})'
    for i in range(len(tracks)):
        first = tracks[i].get('this')
        second = tracks[i].get('next')
        tracks[i]['title'] = get_value(content[first:second], title)
        tracks[i]['performer'] = get_value(content[first:second], perf)
        if tracks[i].get('performer') is None:
            tracks[i]['performer'] = performer
        tracks[i]['index0'] = get_value(
            content[first:second], index0, index=True)
        tracks[i]['index1'] = get_value(
            content[first:second], index1, index=True)
        if first:
            del tracks[i]['this']
        if second:
            del tracks[i]['next']


def extract_metadata(filename, res):
    content = read_file(filename)
    if content is None:
        raise ValueError('cue is not readable or has bad encoding')
    res['album performer'] = get_value(content, r'^PERFORMER +(.+)')
    res['album'] = get_value(content, r'^TITLE +(.+)')
    res['genre'] = get_value(content, r'REM GENRE +(.+)')
    res['disc ID'] = get_value(content, r'^REM DISCID +(.+)')
    res['date'] = get_value(content, r'^REM DATE +(.+)')
    res['comment'] = get_value(content, r'^REM COMMENT +(.+)')
    res['tracks'] = get_tracks(content)
    if res['tracks']:
        get_tracks_meta(content, res['tracks'], res['album performer'])
