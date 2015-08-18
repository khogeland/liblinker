import mutagen
import struct
from mutagen import mp3, flac, mp4
from tinytag import TinyTag as tt
import os
import sys

if len(sys.argv) < 3:
    exit('usage: liblinker in_directory out_directory')

formats = ['mp3', 'flac', 'wav', 'wave', 'm4a', 'aac']
in_dir, out_dir = sys.argv[1], sys.argv[2]
bad_files = False
tags = {}


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def walk(name):
    if os.path.isdir(name):
        for f in os.listdir(name):
            walk('%s/%s' % (name, f))
    else:
        ext = os.path.splitext(name)[1].lower()[1:]
        if ext in formats:
            tags[name] = get_album_artist(name, ext)


def get_album_artist(name, ext, infer=True):
    return {
        'mp3': tags_mp3,
        'flac': tags_flac,
        'm4a': tags_mp4,
        'aac': tags_mp4,
        'wav': tags_wav,
        'wave': tags_wav
    }[ext](name, infer)


def infer_album_artist(name, tag_func):
    parent = os.path.abspath(os.path.join(name, os.pardir))
    raw_tags = []
    for f in os.listdir(parent):
        full_name = '%s/%s' % (parent, f)
        ext = f.split('.')[-1].lower()
        if os.path.isfile(full_name) and ext in formats:
            raw_tags.append(get_album_artist(full_name, ext, False))
    tags = [ t for t in raw_tags if t is not None and t[0] is not None and t[1] is not None]
    artists = list(set(map(lambda x: x[0], tags)))
    albums = list(set(map(lambda x: x[1], tags)))
    i_tags = artists[0] if len(artists) == 1 else None, albums[0] if len(albums) == 1 else None
    if not any(i_tags):
        global bad_files
        bad_files = True
    uprint(i_tags)
    return i_tags


def tags_mp3(name, infer=True):
    try:
        tags = mp3.MP3(name).tags
    except mp3.HeaderNotFoundError:
        if infer:
            uprint('WARN: File appears to be corrupt or malformed, attempting to infer artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name, tags_mp3)
        return None
    if not tags:
        return None, None
    return tags['TPE1'].text[0] if 'TPE1' in tags.keys() else tags['TOPE'] if 'TOPE' in tags.keys() else None,\
           tags['TALB'].text[0] if 'TALB' in tags.keys() else tags['TOAL'] if 'TOAL' in tags.keys() else None


def tags_flac(name, infer=True):
    try:
        tags = flac.FLAC(name)
    except mutagen.flac.FLACNoHeaderError:
        if infer:
            uprint('WARN: File appears to be corrupt or malformed, attempting to infer  artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name, tags_flac)
        return None
    if not tags:
        return None, None
    return tags['album'][0], tags['albumartist'][0] if 'albumartist' in tags.keys() else tags['artist'][0]


def tags_wav(name, infer=True):
    try:
        tags = tt.get(name)
    except struct.error:
        if infer:
            uprint('WARN: File appears to be corrupt or malformed, attempting to infer  artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name, tags_wav)
        return None
    if not tags:
        return None, None
    return tags.artist, tags.album

def tags_mp4(name, infer=True):
    try:
        tags = mp4.MP4(name)
    except mp4.MP4StreamInfoError:
        if infer:
            uprint('WARN: File appears to be corrupt or malformed, attempting to infer  artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name, tags_mp4)
        return None
    if not tags:
        return None, None
    return tags['\xa9alb'][0] if '\xa9alb' in tags.keys() else None,\
           tags['\xa9ART'][0] if '\xa9ART' in tags.keys() else None

walk(in_dir)
uprint(len(tags))
if bad_files:
    uprint('WARN: There are corrupted or mistagged files in your library that could not be organized. '
           'They have been put in "%s/ErrorFiles" so you may organize them manually.' % out_dir)
