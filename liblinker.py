#! python3
import mutagen
import struct
from mutagen import mp3, flac, mp4
from tinytag import TinyTag
import os
import re
import sys

if len(sys.argv) < 3:
    exit('Usage: liblinker IN_DIR OUT_DIR [--silent]')
silent = True if len(sys.argv) == 4 and sys.argv[3] == '--silent' else False
formats = ['mp3', 'flac', 'wav', 'wave', 'm4a', 'aac']
in_dir, out_dir = os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2])
bad_files = False
all_tags = {}
slash = str(os.path.sep)


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    if silent:
        return
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def walk(name):
    if os.path.isdir(name):
        for f in os.listdir(name):
            walk(name + slash + f)
    else:
        ext = os.path.splitext(name)[1].lower()[1:]
        if ext in formats:
            all_tags[name] = get_album_artist(name, ext)


def get_album_artist(name, ext, infer=True):
    return {
        'mp3': tags_mp3,
        'flac': tags_flac,
        'm4a': tags_mp4,
        'aac': tags_mp4,
        'wav': tags_wav,
        'wave': tags_wav
    }[ext](name, infer)


def infer_album_artist(name):
    parent = os.path.abspath(os.path.join(name, os.pardir))
    raw_tags = []
    for f in os.listdir(parent):
        full_name = parent + slash + f
        ext = f.split('.')[-1].lower()
        if os.path.isfile(full_name) and ext in formats:
            raw_tags.append(get_album_artist(full_name, ext, False))
    tags = [t for t in raw_tags if t is not None and t[0] is not None and t[1] is not None]
    artists = list(set(map(lambda x: x[0], tags)))
    albums = list(set(map(lambda x: x[1], tags)))
    i_tags = artists[0] if len(artists) == 1 else None, albums[0] if len(albums) == 1 else None
    if not any(i_tags) or (i_tags[0] is None and i_tags[1] is not None):
        i_tags = None
        global bad_files
        bad_files = True
    uprint(i_tags)
    return i_tags


def tags_mp3(name, infer=True):
    try:
        tags = mp3.MP3(name).tags
    except (mp3.HeaderNotFoundError, mutagen.mp3.error):
        if infer:
            uprint('WARN: Corrupted or mistagged, inferring artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name)
        return None
    if not tags:
        return None, None
    return \
        tags['TPE1'].text[0] if 'TPE1' in tags.keys() else tags['TOPE'] if 'TOPE' in tags.keys() else None,\
        tags['TALB'].text[0] if 'TALB' in tags.keys() else tags['TOAL'] if 'TOAL' in tags.keys() else None


def tags_flac(name, infer=True):
    try:
        tags = flac.FLAC(name)
    except (mutagen.flac.FLACNoHeaderError, mutagen.flac.error):
        if infer:
            uprint('WARN: Corrupted or mistagged, inferring artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name)
        return None
    if not tags:
        return None, None
    return tags['albumartist'][0] if 'albumartist' in tags.keys() else tags['artist'][0] if 'artist' in tags.keys() \
        else None, tags['album'][0] if 'album' in tags.keys() else None


def tags_wav(name, infer=True):
    try:
        tags = TinyTag.get(name)
    except struct.error:
        if infer:
            uprint('WARN: Corrupted or mistagged, inferring artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name)
        return None
    if not tags:
        return None, None
    return tags.artist, tags.album


def tags_mp4(name, infer=True):
    try:
        tags = mp4.MP4(name)
    except (mp4.MP4StreamInfoError, mutagen.mp4.error):
        if infer:
            uprint('WARN: Corrupted or mistagged, inferring artist and album: %s ...' % name, end=' ')
            return infer_album_artist(name)
        return None
    if not tags:
        return None, None
    return \
        tags['\xa9ART'][0] if '\xa9ART' in tags.keys() else None,\
        tags['\xa9alb'][0] if '\xa9alb' in tags.keys() else None


def make_links():
    for path in all_tags:
        if not all_tags[path] or not all_tags[path][0]:
            new_path = out_dir + slash + '_ErrorFiles' + slash + os.path.split(path.replace(in_dir, ''))[0]
        else:
            artist, album = all_tags[path]
            artist = clean(artist)
            album = clean(album) if album else 'Unknown Album'
            new_path = out_dir + slash + artist + slash + album
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        tail = os.path.split(path)[1]
        new_path += slash + clean(tail)
        if not os.path.exists(new_path):
            try:
                os.link(path, new_path)
            except OSError:
                os.symlink(path, new_path)


def clean(string):
    return re.sub(r'\s+$', '', re.sub(r'[<>:"/\\\|\?\*]', '', string))


def main():
    try:
        uprint('INFO: Scanning music library at "%s"' % in_dir)
        walk(in_dir)
        uprint('INFO: Creating links at "%s"' % out_dir)
        make_links()
        if bad_files:
                uprint('WARN: There are corrupted or mistagged files in your library that could not be organized. '
                       'They have been put in "%s%s_ErrorFiles" so you may organize them manually.' % (out_dir, slash))
    except KeyboardInterrupt:
        exit('Interrupted.')


if __name__ == '__main__':
    main()
