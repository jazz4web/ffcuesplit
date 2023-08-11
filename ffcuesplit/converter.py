import re
import shlex

from subprocess import Popen, PIPE


def get_flac(cue, track, opts, filename):
    cmd = 'flac {0}{1}{2}{3} -o "{4}"{5}{6}{7}{8}{9}{10}{11} -'.format(
        opts or '-8',
        ' -f --totally-silent',
        ' --endian=little --channels=2 --sign=signed',
        ' --channels=2 --bps=16 --sample-rate=44100',
        filename,
        f' --tag=artist=\"{track["performer"]}\"',
        f' --tag=album=\"{cue["album"]}\"',
        f' --tag=genre=\"{cue["genre"]}\"',
        f' --tag=title=\"{track["title"]}\"',
        f' --tag=tracknumber=\"{track["num"]}\"',
        f' --tag=date=\"{cue["date"]}\"',
        f' --tag=comment=\"{cue["commentary"]}\"')
    return cmd


def convert(track, cue, arguments):
    ext = {'flac': '.flac', 'mp3': '.mp3', 'vorbis': '.ogg', 'opus': '.opus'}
    f = ext[arguments.media_type]
    if arguments.rename:
        title = re.sub(r'[\\/|?<>*:]', '~', track['title'])
        artist = re.sub(r'[\\/|?<>*:]', '~', track['performer'])
        name = f'{track["num"]} - {artist} - {title}{f}'
    else:
        name = f'{track["num"]}{f}'
    if not arguments.quiet:
        print(name)
    ss = f' -ss {track["start"]}' if track['start'] else ''
    tt = f' -to {track["end"]}' if track['end'] else ''
    stats = ' -stats' if not arguments.quiet else ''
    opts = f' -v quiet{stats} -vn -codec:a pcm_s16le -map_metadata -1'
    ffmpeg = f'ffmpeg{ss}{tt} -i {cue["media"]}{opts} -f s16le -'
    if arguments.media_type == 'flac':
        part = get_flac(cue, track, arguments.enc_opts, name)
#   cmd = f'{ffmpeg} | {part}'
#   print(cmd)
    with Popen(shlex.split(ffmpeg), stdout=PIPE) as f, \
            Popen(shlex.split(part), stderr=PIPE, stdin=f.stdout) as enc:
        enc.communicate()
