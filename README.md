## liblinker ##

This utility creates an organized album -> artist -> track directory structure from a given folder containing music files. If you would like to have an organized library (or need one, if you're using something like Subsonic which relies on directory structure) but are unable to move the source files (e.g. you do not have permission or you are seeding them in a BitTorrent client), this is for you. Can also be used to merge multiple music libraries.

Also supports moving or copying instead of linking, if you're into that sort of thing...
 
Supported formats: *MP3, FLAC, Wave, MP4 (M4A/AAC)*

Requires Python 3.4+

Hard links are used when possible, otherwise symlinks are used.
 
### Installation ###

```
pip install liblinker
```

or

```
pip install git+https://github.com/btym/liblinker
```

### Usage ###

```
Usage: liblinker IN_DIR OUT_DIR [--silent] [--mode=link]

--mode=
        link    Creates links to the source files in the target directory. This is the default behavior.
        copy    Copies source files to the target directory, keeping original files.
        move    Moves source files from the source directory to the target directory.

--silent        All output will be suppressed except for error messages.

```
