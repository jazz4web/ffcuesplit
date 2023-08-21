"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
name: ffcuesplit
description: a simple CDDA splitter
license: GNU GPLv3
author: Jazz
contacts: webmaster@codej.ru
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import argparse
import os
import sys

from .checker import check_couple, check_cue, get_points
from .converter import convert
from .parser import extract_metadata, make_couple
from .system import check_dep


def parse_args(version):
    args = argparse.ArgumentParser()
    args.add_argument(
        '-v', '--version', action='version', version=version)
    args.add_argument(
        '-g',
        action='store',
        dest='gaps',
        default='split',
        choices=('append', 'prepend', 'split'),
        help='control gaps, default is `split`')
    args.add_argument(
        '-m',
        action='store',
        dest='media_type',
        default='flac',
        choices=('flac', 'opus', 'vorbis', 'mp3'),
        help='the output media type, default is flac')
    args.add_argument(
        '-o',
        action='store',
        dest='enc_opts',
        help='control some options while encoding tracks')
    args.add_argument(
        '-r',
        action='store_true',
        dest='rename',
        default=False,
        help='rename tracks')
    args.add_argument(
        '-q',
        action='store_true',
        dest='quiet',
        default=False,
        help='show no output')
    args.add_argument(
        'cue_file', action='store', help='the converted file name')
    return args.parse_args()


def show_error(msg, code=1):
    print(
        os.path.basename(sys.argv[0]),
        'error',
        msg,
        sep=':',
        file=sys.stderr)
    sys.exit(code)


def start_the_process(arguments):
    meta = dict()
    make_couple(arguments.cue_file, meta)
    cue, media = meta.get('cue'), meta.get('media')
    if not check_dep('ffmpeg'):
        raise OSError('ffmpeg is not installed')
    if arguments.media_type == 'flac':
        if not check_dep('flac'):
            raise OSError('flac is not installed')
    elif arguments.media_type == 'opus':
        if not check_dep('opusenc'):
            raise OSError('opus-tools is not installed')
    elif arguments.media_type == 'vorbis':
        if not check_dep('oggenc'):
            raise OSError('vorbis-tools is not installed')
    elif arguments.media_type == 'mp3':
        if not check_dep('lame'):
            raise OSError('lame is not installed')
    extract_metadata(cue, meta)
    check_cue(meta)
    check_couple(meta)
    get_points(meta, arguments.gaps)
    for each in meta['tracks']:
        convert(each, meta, arguments)
