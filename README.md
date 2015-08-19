## liblinker ##

This utility creates an organized album -> artist -> track directory structure from a given folder containing music files. If you would like to have an organized library (or need one, if you're using something like Subsonic which relies on directory structure) but are unable to move the source files (e.g. you do not have permission or you are seeding them in a BitTorrent client), this is for you.
 
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
liblinker IN_DIR OUT_DIR [--silent]
```

`IN_DIR` is the folder containing all your music files.

`OUT_DIR` is the folder that liblinker will put the organized folder structure in.

`--silent` suppresses all output.
