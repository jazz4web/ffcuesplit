import shlex

from subprocess import Popen, PIPE


def convert(track, cue):
    print(f'track{track["num"]}')
    if track['start']:
        ss = f' -ss {track["start"]}'
    else:
        ss = ''
    if track['end']:
        tt = f' -to {track["end"]}'
    else:
        tt = ''
    cmd = 'ffmpeg{0}{1} -i {2} -v quiet -stats -codec:a pcm_s16le {3}'.format(
            ss, tt, cue['media'], 'track' + track['num'] + '.wav')
    with Popen(shlex.split(cmd)) as ffmpeg:
        res = ffmpeg.communicate()
