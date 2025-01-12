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

More information is available on my [web-site](https://avm4.ru/xixiLkLT) or
with the key --help in terminal.

```
ffcuesplit --help
```

This code is free, you can use ffcuesplit in accordance with GNU GPLv3. Be
aware, some [donation](https://yoomoney.ru/to/410015590807463) would be
excellent.
