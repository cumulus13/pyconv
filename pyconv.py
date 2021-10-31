#!/usr/bin/env python

import cloudconvert
import sys
from pprint import pprint
from progressbar import ProgressBar
from make_colors import make_colors
from pydebugger.debug import debug
import clipboard
import os
from datetime import datetime
import time
from configset import configset
import argparse
try:
    from pause import pause
except:
    def pause(*args, **kwargs):
        raw_input("Enter to continue")

class PyConv(object):
    configname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pyconv.ini')
    config = configset(configname)
    prefix = "{variables.task} >> {variables.subtask}"
    variables = {'task': '', 'subtask': ''}
    bar = ProgressBar(max_value = 100, max_error = False, prefix = prefix, variables = variables)
    
    api = config.get_config('auth', 'api') or "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2M1YzNhYjVlNmZkY2EzMWFiYTE3MzM4Njg4ZWVhMjZkY2EzYTQzOTgxOTBjOWE1YzRjNDBhZjZmMzMyYjQwMWY2ZTMxNDI3MmJhYzVjYTQiLCJpYXQiOjE2MzU1ODkzNjQuNDQ0NzExLCJuYmYiOjE2MzU1ODkzNjQuNDQ0NzE1LCJleHAiOjQ3OTEyNjI5NjQuNDIxMDA3LCJzdWIiOiI1MTYxNzEzIiwic2NvcGVzIjpbInVzZXIucmVhZCIsInVzZXIud3JpdGUiLCJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIiwid2ViaG9vay5yZWFkIiwid2ViaG9vay53cml0ZSIsInByZXNldC5yZWFkIiwicHJlc2V0LndyaXRlIl19.iVY2yGuwXgG1cESYckvFxf_8LiqQm041NnuDTTcA2zogw-Dj05z8El7N2Vl74k_pjOpPOTrN234uxGU-GcbPT-ajvztbbj2SbZHOKJ2q_fmSPfiNIVN3JiU8DeQRGGXJfXPjwRwaACOYo6Ce4fOLPjphEfgXNl6vHSo2IpqtiXahKBCsE54QlBTu7birsC8aaiBO_rQyxGVva_3tJzwePAq1gEHU3Qy3a7JI8CVXkaOfUHUP8ERdbgOVO-PpS2TpTZJUgDlgl0WFSfr1aj0pKDbh84rcH1itnyRd3vgMUAC2tRbCIP8x2bbk01UDMUc-IsSLYB3LfS7JQphuySlZtFzcQbGVeNzbwDAjSDxOf4HGvVL3_eAasFNGNXm1MslN-4KtEjlrOlViJ1yQgM6tSvo4ixMdB1AmjfXNTE1Op8pzCXdxCzEBQEbH4FfPAsPCfqaA0zjK3TI3SOghweJqbp3uDS4q4nHe26FG-tQmI-zM-5c2Q7hYwzNH9WhUb01Lmq5xU3Kbzd_WjzZsTP6Dfk0dg2u6sGzSE0woe6xgGSShYNZsUIo-bBo6mFgPS0ckE8zmfEWyf3u-ZOZN7OATNTcaSkPnvQh8F2OkwaNfBZUawbXoOdf1ooYjJneGdAkT3l6RESBIdQNZYpFWN1u3-SQrl2RjnkvBYsZdF5fJgJc"
    debug(api = api)
    url = None
    if not api:
        print(make_colors("No API !", 'lw', 'r'))
        sys.exit()

    def __init__(self, api = None, url = None, configname = None):
        super(PyConv, self)
        self.api = api or self.api
        url = url or self.url
        if configname:
            self.config(configname)
            
    @classmethod
    def make_tasks(self, suffix = None):
        suffix = suffix or str(self.set_time())
        tasks = {
            "tasks": {
                 'import-{}'.format(suffix): {
                      'operation': 'import/url',
                      'url': self.url
                 },
                 'convert-{}'.format(suffix): {
                     'operation': 'convert',
                     'input': 'import-{}'.format(suffix),
                     'output_format': 'mkv',
                     #'input_format': 'mp4',
                     'video_codec':'x264',
                     'crf':37,
                     'preset':'fast',
                     'tune':'animation',
                     'profile':'baseline',
                     'level':1,
                     'audio_codec':'copy',
                     'audio_bitrate':64
                 },
                 'export-{}'.format(suffix): {
                     'operation': 'export/url',
                     'input': 'convert-{}'.format(suffix)
                 }
             }
        }
        debug(tasks = tasks)
        self.suffix = suffix
        self.tasks = tasks
        return tasks
        
    @classmethod    
    def set_time(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S-%f')

    @classmethod
    def usage(self):
        parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter)
        parser.add_argument("URL", help = 'Url convert to', action = 'store')
        parser.add_argument('-crf', '--crf', help = 'The Constant Rate Factor (CRF) sets the quality of the video. The range of the CRF scale is 0-51, where 0 is lossless, 23 is the default, and 51 is worst quality possible. Defaults to 23', action = 'store', default = 23, type = int)
        parser.add_argument('-l', '--level', help = "Set output to a specific H264 compatibility profile level. Possible values: 1, 1b, 1.1, 1.2, 1.3, 2.0, 2.1, 2.2, 3.0, 3.1, 3.2, 4.0, 4.1, 4.2, 5.0, 5.1, 5.2, default to 1", action = 'store', default = 1, type = int)
        parser.add_argument('-tn', '--tune', help = 'Settings based upon the specifics of your input. Possible values: film, animation, grain, stillimage, fastdecode, zerolatency, psnr, ssim. Defaults to "animation"', action = 'store', default = "animation")
        parser.add_argument('-pf', '--profile', help = "Set output to a specific H264 compatibility profile. Possible values: baseline, main, high, high10, high422, high444. Defaults to 'baseline'", action = 'store', default = "baseline", type = str)
        parser.add_argument('-if', '--input-format', help = "The current format of the file, e.g. pdf. If not set, the extension of the input file is used as input format. [not require/optional]", action = 'store')
        parser.add_argument('-of', '--output-format', help = "The target format to convert to. [require]", action = 'store', required = True)
        parser.add_argument('-o', '--save-as', help = "Choose a filename (including extension) for the output file. If the conversion produces multiple output files, printf style placeholders are possible (e.g. myfile-%%d.pdf produces the output files myfile-1.pdf, myfile-2.pdf and so on).", action = 'store')
        parser.add_argument('-t', '--timeout', help = "Timeout in seconds after the task will be cancelled. By default, tasks time out after 5 hours.", action = 'store')
        parser.add_argument('-vc', '--video-codec', help = 'Codec to encode the video. Use "copy" to copy the stream without re-encoding. Defaults to x264. Possible values: copy, x264, x265, vp8, vp9, av1.', action = 'store')
        parser.add_argument('-W', '--width', help = "Set output video width resolution.", type = int, action = 'store')
        parser.add_argument('-H', '--height', help = "Set output video height resolution.", type = int, action = 'store')
        parser.add_argument('-fps', '--fps', help = "Change the video frame rate.", type = float, action = 'store')
        parser.add_argument('-ar', '--aspect-ratio', help = "Change the video aspect ratio, for example to 16:9 or 4:3.", action = 'store')
        parser.add_argument('-sm', '--subtitles-mode', help = 'Add hardsubs or softsubs to the video. "copy" copies the softsubs from the input file. Defaults to none. Possible values: none, copy, soft, hard.', action = "store")
        parser.add_argument('-s', '--subtitle', help = 'Add subtitles by selecting a SRT or ASS file. Only has an effect, if "Subtitles Mode" is set to "soft" or "hard"', action = 'store')
        parser.add_argument("-ac", '--audio-codec', help = 'Codec to encode the audio. Use "copy" to copy the stream without re-encoding. Defaults to copy. Possible values: copy, none, aac, aac_he_1, aac_he_2, opus, vorbis', action = 'store', default = "copy")
        parser.add_argument("-ab", '--audio-bitrate', help = "Audio bitrate. Defaults to 64.", default = 64, type = int)
        parser.add_argument("-v", '--volume', help = "Change the audio volume, whereas 1.0 is the current volume. Example: a value of 1.1 increases the volume by 10%%.", action = 'store')
        parser.add_argument("-ts", '--trim-start', help = "Trim start timestamp (HH:MM:SS)", action = 'store')
        parser.add_argument('-td', '--trim-end', help = "Trim end timestamp (HH:MM:SS)", action = 'store')
        parser.add_argument('-pr', '--preset', help = "The preset is a collection of options that will provide a certain encoding speed to compression ratio. Defaults to medium. Possible values: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow.", action = 'store')
        
        if len(sys.argv) == 1:
            parser.print_usage()
        else:
            args = parser.parse_args()
            
            if not hasattr(self, "tasks"):
                self.tasks = self.make_tasks()
            self.tasks['tasks']["import-" + self.suffix]['url'] = args.URL
            if args.crf:
                if args.crf in range(52):
                    self.tasks['tasks']["convert-" + self.suffix]['crf'] = args.crf
            if args.level:
                if args.level in [1, "1b", 1.1, 1.2, 1.3, 2.0, 2.1, 2.2, 3.0, 3.1, 3.2, 4.0, 4.1, 4.2, 5.0, 5.1, 5.2]:
                    self.tasks['tasks']["convert-" + self.suffix]['level'] = args.level
            if args.tune:
                if args.tune in ["film", "animation", "grain", "stillimage", "fastdecode", "zerolatency", "psnr", "ssim"]:
                    self.tasks['tasks']["convert-" + self.suffix]['tune'] = args.tune
            if args.profile:
                if args.profile in ["baseline", "main", "high", "high10", "high422", "high444"]:
                    self.tasks['tasks']["convert-" + self.suffix]['profile'] = args.profile
            if args.input_format:
                self.tasks['tasks']["convert-" + self.suffix]['input_format'] = args.input_format
            if args.output_format:
                self.tasks['tasks']["convert-" + self.suffix]['output_format'] = args.output_format
            if args.save_as:
                self.tasks['tasks']["convert-" + self.suffix]['filename'] = args.save_as
            if args.timeout:
                self.tasks['tasks']["convert-" + self.suffix]['timeout'] = args.timeout
            if args.video_codec:
                if args.video_codec in ["copy", "x264", "x265", "vp8", "vp9", "av1"]:
                    self.tasks['tasks']["convert-" + self.suffix]['video_codec'] = args.video_codec
            if args.width:
                self.tasks['tasks']["convert-" + self.suffix]['width'] = args.width
            if args.height:
                self.tasks['tasks']["convert-" + self.suffix]['height'] = args.height
            if args.fps:
                self.tasks['tasks']["convert-" + self.suffix]['fps'] = args.fps
            if args.aspect_ratio:
                self.tasks['tasks']["convert-" + self.suffix]['aspect_ratio'] = args.aspect_ratio
            if args.subtitles_mode:
                if args.subtitles_mode in ["none", "copy", "soft", "hard"]:
                    self.tasks['tasks']["convert-" + self.suffix]['subtitles_mode'] = args.subtitles_mode
            if args.subtitle:
                self.tasks['tasks']["convert-" + self.suffix]['subtitle'] = args.subtitle
            if args.audio_codec:
                self.tasks['tasks']["convert-" + self.suffix]['audio_codec'] = args.audio_codec
            if args.audio_bitrate:
                self.tasks['tasks']["convert-" + self.suffix]['audio_bitrate'] = args.audio_bitrate
            if args.volume:
                self.tasks['tasks']["convert-" + self.suffix]['volume'] = args.volume
            if args.trim_start:
                try:
                    datetime.strptime(args.trim_start, "%H:%M:%S")
                    self.tasks['tasks']["convert-" + self.suffix]['trim_start'] = args.trim_start
                except:
                    pass
            if args.trim_end:
                try:
                    datetime.strptime(args.trim_end, "%H:%M:%S")
                    self.tasks['tasks']["convert-" + self.suffix]['trim_end'] = args.trim_end
                except:
                    pass
            if args.preset:
                if args.preset in ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"]:
                    self.tasks['tasks']["convert-" + self.suffix]['preset'] = args.preset
            
            debug(self_task = self.tasks)
            self.convert()

    @classmethod
    def convert(self, url = None):
        cloudconvert.configure(api_key = self.api)
        if not hasattr(self, "tasks"):
            self.tasks = self.make_tasks()        
        if url == 'c':
            url = clipboard.paste()
        if not url:
            url = self.tasks['tasks']["import-" + self.suffix]['url']
        debug(url = url)
        if not url or not "http" == url[:4]:
            self.bar.update(100, task = make_colors("[Convert] No URL ! [1]", 'lw', 'r'), subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
            print(make_colors("No URL !", 'lw', 'r'))
            sys.exit()
        
        #url = "https://srv6.racaty.net:183/d/qmflvksl6xjz7x5iywlyjyid2bm24xycoadjypulz7wku7aqnteyhxrncw3dom7s64dh6hvu/Otakudesu.vip_DQ--55_480p.mp4"
        debug(url = url)
        task = make_colors("Create", 'lw', 'bl')
        subtask = make_colors("Jobs", 'b', 'lg') + " "
        
        if not hasattr(self, "tasks"):
            print(make_colors("No Tasks !", 'lw', 'r'))
            sys.exit()
        
        self.bar.update(1, task = task, subtask = subtask)        
        jobs = cloudconvert.Job.create(payload=self.tasks)
        debug(jobs = jobs)
        if not jobs:
            print(make_colors("ERROR Converting !", 'lw', 'r'))
            sys.exit()
        if not jobs.get('status') == 'waiting':
            debug(jobs = jobs, debug = True)
            pprint(jobs)
            sys.exit()
        self.bar.update(75, task = task, subtask = subtask)
        import_data = filter(lambda k: k.get('operation') == 'import/url', jobs['tasks'])[0]
        debug(import_data = import_data)
        import_id = import_data['id']
        debug(import_id = import_id)
        
        convert_data = filter(lambda k: k.get('operation') == 'convert', jobs['tasks'])[0]
        debug(convert_data = convert_data)
        convert_id = convert_data['id']
        debug(convert_id = convert_id)
        
        export_data = filter(lambda k: k.get('operation') == 'export/url', jobs['tasks'])[0]
        debug(export_data = export_data)
        export_id = export_data['id']
        debug(export_id = export_id)
        #print("import_id:", import_id)
        #print("convert_id:", convert_id)
        #print("export_id:", export_id)
        self.bar.update(100, task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
        
        import_error = False
        convert_error = False
        export_error = False
        
        task = make_colors("Import", 'lw', 'bl')
        subtask = make_colors("URL", 'b', 'lg') + " "
        self.bar.update(10, task = task, subtask = subtask)
        
        import_task = cloudconvert.Task.show(id=import_id)
        debug(import_task = import_task)
        n = 1
        if import_task.get('status') == 'error':
            print(make_colors("Upload File/URL ERROR", 'lw', 'r') + " " + make_colors("or", 'lc') + " " + make_colors("Invalid URL !", 'lw', 'm') + " " + make_colors("[" + import_task.get(
                "code") + "]", 'b', 'y'))
            return False        
        while 1:
            debug(import_task = import_task)
            if import_task.get('status') == 'error':
                self.bar.update(100, task = task, subtask = make_colors("[" + import_task.get("code") + "]", 'lw', 'r') + " ")                
                print(make_colors("Upload File/URL ERROR", 'lw', 'r') + " " + make_colors("or", 'lc') + " " + make_colors("Invalid URL !", 'lw', 'm') + " " + make_colors("[" + import_task.get("code") + "]", 'b', 'y'))
                return False                    
            elif import_task:
                if not import_task.get('status') == 'finished':
                    self.bar.update(n, task = task, subtask = subtask)
                    n += 1
                    import_task = cloudconvert.Task.show(id=import_id)
                else:
                    self.bar.update(import_task.get('percent'), task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
                    break
            else:
                self.bar.update(100, task = task, subtask = make_colors("ERROR !", 'lw', 'lr') + " ")
                import_error = True
                break
        
        if import_error:
            print(make_colors("ERROR import URL !", 'lw', 'r'))
            sys.exit()
        self.bar.update(100, task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
        task = make_colors("Convert", 'lw', 'bl')
        subtask = ""
        if import_task.get('result'):
            subtask = make_colors(import_task.get('result').get('files')[0].get('filename'), 'b', 'lg') + " "
        
        self.bar.update(10, task = task, subtask = subtask)
        convert_task = cloudconvert.Task.show(id=convert_id)
        debug(convert_task = convert_task )
        if convert_task.get('result'):
            subtask = make_colors(convert_task.get('result').get('files')[0].get('filename'), 'b', 'lg') + " "
        n = 1
        if convert_task.get('status') == 'error':
            self.bar.update(100, task = task, subtask = make_colors("[" + convert_task.get(
                "code") + "]", 'lw', 'r') + " ")
            print(make_colors("Import File ERROR", 'lw', 'r') + " " + make_colors("or", 'lc') + " " + make_colors("Invalid URL !", 'lw', 'm') + " " + make_colors("[" + convert_task.get(
                "code") + "]", 'b', 'y'))
            return False
        while 1:
            debug(convert_task = convert_task )
            if convert_task.get('status') == 'error':
                self.bar.update(100, task = task, subtask = make_colors("[" + convert_task.get(
                    "code") + "]", 'lw', 'r') + " ")
                print(make_colors("Import File ERROR", 'lw', 'r') + " " + make_colors("or", 'lc') + " " + make_colors("Invalid URL !", 'lw', 'm') + " " + make_colors("[" + convert_task.get(
                    "code") + "]", 'b', 'y'))
                return False            
            elif import_task.get('result'):
                subtask = make_colors(import_task.get('result').get('files')[0].get('filename'), 'b', 'lg') + " "
            elif convert_task.get('result'):
                subtask = make_colors(convert_task.get('result').get('files')[0].get('filename'), 'b', 'lg') + " "
            if convert_task:
                if not convert_task.get('status') == 'finished':
                    self.bar.update(n, task = task, subtask = subtask)
                    n += 1
                    convert_task = cloudconvert.Task.show(id=convert_id)
                else:
                    self.bar.update(convert_task.get('percent'), task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
                    break
            else:
                self.bar.update(100, task = task, subtask = make_colors("ERROR !", 'lw', 'lr') + " ")
                convert_error = True
                break
        
        if convert_error:
            print(make_colors("ERROR Convert URL !", 'lw', 'r'))
            sys.exit()
        self.bar.update(100, task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
        task = make_colors("Export", 'lw', 'bl')
        subtask = make_colors("URL", 'b', 'lg') + " "
        self.bar.update(10, task = task, subtask = subtask)
        export_task = cloudconvert.Task.show(id=export_id)
        debug(export_task = export_task)
        n = 1
        if export_task.get('status') == 'error':
            print(make_colors("Export Task ERROR", 'lw', 'r') + " " + make_colors("[" + export_task.get(
                "code") + "]", 'b', 'y'))
            return False        
        while 1:
            debug(export_task = export_task)
            if export_task.get('status') == 'error':
                self.bar.update(100, task = task, subtask = make_colors("[" + export_task.get("code") + "]", 'lw', 'r') + " ")
                print(make_colors("Export Task ERROR", 'lw', 'r') + " " + make_colors("[" + export_task.get("code") + "]", 'b', 'y'))
                return False                    
            elif export_task:
                if not export_task.get('status') == 'finished':
                    self.bar.update(n, task = task, subtask = subtask)
                    n += 1
                    export_task = cloudconvert.Task.show(id=export_id)
                else:
                    self.bar.update(export_task.get('percent'), task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
                    break
            else:
                self.bar.update(100, task = task, subtask = make_colors("ERROR !", 'lw', 'lr') + " ")
                export_error = True
                break
        
        if export_error:
            print(make_colors("ERROR get download URL !", 'lw', 'r'))
            sys.exit()
        self.bar.update(100, task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
        download_link = ''
        task = make_colors("Get", 'lw', 'bl')
        subtask = make_colors("Download URL", 'b', 'lg') + " "
        self.bar.update(10, task = task, subtask = subtask)
        n = 10
        while 1:
            try:
                file_export_result = export_task.get("result").get("files")[0]
                debug(file_export_result = file_export_result)
                #download_link = cloudconvert.download(filename=file_export_result['filename'], url = file_export_result['url'])
                download_link = file_export_result.get('url')
                debug(download_link = download_link)
                self.bar.update(100, task = task, subtask = make_colors("FINISH !", 'lw', 'lr') + " ")
                if download_link:
                    break
                else:
                    export_task = cloudconvert.Task.show(id=export_id)
                    debug(export_task = export_task)
            except:
                export_task = cloudconvert.Task.show(id=export_id)
                debug(export_task = export_task)
                self.bar.update(n, task = task, subtask = subtask)
                n += 1
                time.sleep(1)
        if download_link:
            print(make_colors("DOWNLOAD_LINK:", 'b', 'y') + " " + make_colors(download_link, 'b', 'lg'))
            clipboard.copy(download_link)
        else:
            print(make_colors("DOWNLOAD_LINK:", 'b', 'y') + " " + make_colors("ERROR", 'lw', 'r'))
        return download_link
        #res = cloudconvert.Task.show(id=export_id)
        #pprint(res)
        #file = res.get("result").get("files")[0]
        #pprint(file)
        #res = cloudconvert.download(filename=file['filename'], url = file['url'])
        #pprint(res)
def usage():
    return PyConv.usage()

if __name__ == "__main__":
    PyConv.usage()