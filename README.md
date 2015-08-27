## liblinker ##

This utility creates an organized album -> artist -> track directory structure from a given folder containing music files. If you…

-  Want to organize your massive torrent folder while keeping everything
   seeding
-  Want to merge multiple music folders into one location
-  Don’t have permission to move the original files
-  Want to keep iTunes files or other junky application files out of
   your original library (use liblinker -> point iTunes/whatever at the
   output directory)

This is for you.

Hard links are used when possible, otherwise symlinks are used. Also supports moving or copying instead of linking, if you're into that sort of thing...
 
Supported formats: *MP3, FLAC, Wave, MP4 (M4A/AAC)*

Requires Python 3.4+
 
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
liblinker IN_DIR OUT_DIR [--silent] [--mode=link]

--mode=
        link    Creates links to the source files in the target directory. This is the default behavior.
        copy    Copies source files to the target directory, keeping original files.
        move    Moves source files from the source directory to the target directory.

--silent        All output will be suppressed except for error messages.

```
