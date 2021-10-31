pycon
==========

Online video converter via cloudconverter.com
------------------------------------------------

usage
==========
```bash
    usage: pycon.py [-h] [-crf CRF] [-l LEVEL] [-tn TUNE] [-pf PROFILE]
                    [-if INPUT_FORMAT] -of OUTPUT_FORMAT [-o SAVE_AS] [-t TIMEOUT]
                    [-vc VIDEO_CODEC] [-W WIDTH] [-H HEIGHT] [-fps FPS]
                    [-ar ASPECT_RATIO] [-sm SUBTITLES_MODE] [-s SUBTITLE]
                    [-ac AUDIO_CODEC] [-ab AUDIO_BITRATE] [-v VOLUME]
                    [-ts TRIM_START] [-td TRIM_END] [-pr PRESET]
                    URL

    positional arguments:
      URL                   Url convert to

    optional arguments:
      -h, --help            show this help message and exit
      -crf CRF, --crf CRF   The Constant Rate Factor (CRF) sets the quality of the
                            video. The range of the CRF scale is 0-51, where 0 is
                            lossless, 23 is the default, and 51 is worst quality
                            possible. Defaults to 23
      -l LEVEL, --level LEVEL
                            Set output to a specific H264 compatibility profile
                            level. Possible values: 1, 1b, 1.1, 1.2, 1.3, 2.0,
                            2.1, 2.2, 3.0, 3.1, 3.2, 4.0, 4.1, 4.2, 5.0, 5.1, 5.2,
                            default to 1
      -tn TUNE, --tune TUNE
                            Settings based upon the specifics of your input.
                            Possible values: film, animation, grain, stillimage,
                            fastdecode, zerolatency, psnr, ssim. Defaults to
                            "animation"
      -pf PROFILE, --profile PROFILE
                            Set output to a specific H264 compatibility profile.
                            Possible values: baseline, main, high, high10,
                            high422, high444. Defaults to 'baseline'
      -if INPUT_FORMAT, --input-format INPUT_FORMAT
                            The current format of the file, e.g. pdf. If not set,
                            the extension of the input file is used as input
                            format. [not require/optional]
      -of OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                            The target format to convert to. [require]
      -o SAVE_AS, --save-as SAVE_AS
                            Choose a filename (including extension) for the output
                            file. If the conversion produces multiple output
                            files, printf style placeholders are possible (e.g.
                            myfile-%d.pdf produces the output files myfile-1.pdf,
                            myfile-2.pdf and so on).
      -t TIMEOUT, --timeout TIMEOUT
                            Timeout in seconds after the task will be cancelled.
                            By default, tasks time out after 5 hours.
      -vc VIDEO_CODEC, --video-codec VIDEO_CODEC
                            Codec to encode the video. Use "copy" to copy the
                            stream without re-encoding. Defaults to x264. Possible
                            values: copy, x264, x265, vp8, vp9, av1.
      -W WIDTH, --width WIDTH
                            Set output video width resolution.
      -H HEIGHT, --height HEIGHT
                            Set output video height resolution.
      -fps FPS, --fps FPS   Change the video frame rate.
      -ar ASPECT_RATIO, --aspect-ratio ASPECT_RATIO
                            Change the video aspect ratio, for example to 16:9 or
                            4:3.
      -sm SUBTITLES_MODE, --subtitles-mode SUBTITLES_MODE
                            Add hardsubs or softsubs to the video. "copy" copies
                            the softsubs from the input file. Defaults to none.
                            Possible values: none, copy, soft, hard.
      -s SUBTITLE, --subtitle SUBTITLE
                            Add subtitles by selecting a SRT or ASS file. Only has
                            an effect, if "Subtitles Mode" is set to "soft" or
                            "hard"
      -ac AUDIO_CODEC, --audio-codec AUDIO_CODEC
                            Codec to encode the audio. Use "copy" to copy the
                            stream without re-encoding. Defaults to copy. Possible
                            values: copy, none, aac, aac_he_1, aac_he_2, opus,
                            vorbis
      -ab AUDIO_BITRATE, --audio-bitrate AUDIO_BITRATE
                            Audio bitrate. Defaults to 64.
      -v VOLUME, --volume VOLUME
                            Change the audio volume, whereas 1.0 is the current
                            volume. Example: a value of 1.1 increases the volume
                            by 10%.
      -ts TRIM_START, --trim-start TRIM_START
                            Trim start timestamp (HH:MM:SS)
      -td TRIM_END, --trim-end TRIM_END
                            Trim end timestamp (HH:MM:SS)
      -pr PRESET, --preset PRESET
                            The preset is a collection of options that will
                            provide a certain encoding speed to compression ratio.
                            Defaults to medium. Possible values: ultrafast,
                            superfast, veryfast, faster, fast, medium, slow,
                            slower, veryslow.
```
Author
=========
[cumulus13](cumulus13@gmail.com)

Requirements
==============
 - cloudconvert
 - progressbar2
 - make_colors
 - clipboard
 - pydebugger
 - configset

