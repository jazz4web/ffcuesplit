import re
import shlex

from subprocess import Popen, PIPE


def get_lame(cue, track, opts, filename):
    cmd = 'lame{0}{1}{2}{3}{4}{5}{6}{7}{8} - "{9}"'.format(
        opts or ' -V 0 --lowpass -1 --noreplaygain',
        ' -r -s 44.1 --quiet --id3v2-only --id3v2-utf16',
        f' --ta \"{track["performer"]}\"',
        f' --tl \"{cue["album"]}\"',
        f' --tg \"{cue["genre"]}\"',
        f' --tt \"{track["title"]}\"',
        f' --tn \"{track["num"]}\"',
        f' --ty \"{cue["date"]}\"',
        f' --tv \"COMM=={cue["commentary"]}\"',
        filename)
    return cmd


def get_vorbis(cue, track, opts, filename):
    cmd = 'oggenc{0}{1}{2}{3}{4}{5}{6}{7}{8} -o \"{9}\" -'.format(
        opts or ' -q 4',
        f' --artist \"{track["performer"]}\"',
        f' --album \"{cue["album"]}\"',
        f' --genre \"{cue["genre"]}\"',
        f' --title \"{track["title"]}\"',
        f' --comment tracknumber=\"{track["num"]}\"',
        f' --date \"{cue["date"]}\"',
        f' --comment comment=\"{cue["commentary"]}\"',
        ' --quiet --raw --raw-rate 44100 --ignorelength',
        filename)
    return cmd


def get_opus(cue, track, opts, filename):
    cmd = 'opusenc{0}{1}{2}{3}{4}{5}{6}{7}{8} - \"{9}\"'.format(
        opts or '',
        f' --artist \"{track["performer"]}\"',
        f' --album \"{cue["album"]}\"',
        f' --genre \"{cue["genre"]}\"',
        f' --title \"{track["title"]}\"',
        f' --comment tracknumber=\"{track["num"]}\"',
        f' --date \"{cue["date"]}\"',
        f' --comment comment=\"{cue["commentary"]}\"',
        ' --quiet --raw --raw-rate 44100 --ignorelength',
        filename)
    return cmd


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
    stats = ' -stats' if not arguments.quiet else ''
    ffmpeg = 'ffmpeg{0}{1} -i "{2}"{3} -f s16le -'.format(
        f' -ss {track["start"]}' if track['start'] else '',
        f' -to {track["end"]}' if track['end'] else '',
        cue['media'],
        f' -v quiet{stats} -vn -codec:a pcm_s16le -map_metadata -1')
    if arguments.media_type == 'flac':
        part = get_flac(cue, track, arguments.enc_opts, name)
    elif arguments.media_type == 'opus':
        part = get_opus(cue, track, arguments.enc_opts, name)
    elif arguments.media_type == 'vorbis':
        part = get_vorbis(cue, track, arguments.enc_opts, name)
    elif arguments.media_type == 'mp3':
        part = get_lame(cue, track, arguments.enc_opts, name)
#   cmd = f'{ffmpeg} | {part}'
#   print(cmd)
    with Popen(shlex.split(ffmpeg), stdout=PIPE) as f, \
            Popen(shlex.split(part), stderr=PIPE, stdin=f.stdout) as enc:
        enc.communicate()
    if enc.returncode:
        raise RuntimeError('something bad happened')
