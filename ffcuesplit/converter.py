import shlex

from subprocess import Popen, PIPE


def convert(track, cue):
    print(f'{track["num"]} - {track["performer"]} - {track["title"]}')
    if track['start']:
        ss = f' -ss {track["start"]}'
    else:
        ss = ''
    if track['end']:
        tt = f' -to {track["end"]}'
    else:
        tt = ''
    cmd = 'ffmpeg{0}{1} -i {2} -v quiet -stats -vn -codec:a pcm_s16le -map_metadata -1 {3}'.format(
            ss, tt, cue['media'], track['num'] + '.wav')
    with Popen(shlex.split(cmd)) as ffmpeg:
        res = ffmpeg.communicate()
