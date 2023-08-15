ffcuesplit is a simple CDDA splitter, it uses ffmpeg decoders.

ffcuesplit works fine on current Debian sid, I did not test it
on Debian stable yet. It requires following packages:

* python3-chardet;
* ffmpeg;
* flac, opus-tools, vorbis-tools, lame.

ffcuesplit can split CDDA-images, cuesheet file is mandatory.

```
ffcuesplit sample.cue
```

Or

```
ffcuesplit sample.flac
```

More information is available with the key --help.

```
ffcuesplit --help
```

This code is free, you can use ffcuesplit in accordance with GNU GPLv3.
