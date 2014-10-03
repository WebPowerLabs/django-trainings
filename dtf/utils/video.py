import os
from datetime import datetime
from subprocess import Popen
from django.conf import settings
import uuid


def convert_video(file_path, format):
    """
    Receives path to the video file and format in which it should be converted.
    Returns path to converted file.
    """
    if format not in ['webm', 'mp4']:
        raise ValueError('Argument "format" value must be "webm" or "mp4".')
    tmp_path = 'tmp/{}'.format(datetime.now().strftime('%Y/%m/%d/'))
    file_name = os.path.basename(file_path
                                 ).split('.')[:-1][0] + '_{}'.format(uuid.uuid4(
                                                                       ).hex)
    out_file_path = os.path.join(settings.MEDIA_ROOT, tmp_path,
                                 file_name + '.{}'.format(format))
    mp4_cmd = ['ffmpeg', '-i', file_path, '-b:v', '1500k', '-codec:v',
               'libx264', out_file_path]
    webm_cmd = ['ffmpeg', '-i', file_path, '-b:v', '1500k', '-codec:v',
                'libvpx', '-codec:a', 'libvorbis', '-b:a', '160000', '-f',
                'webm', '-g', '30', out_file_path]
    command = {'mp4': mp4_cmd, 'webm': webm_cmd}
    pipe = Popen(command[format])
    pipe.wait()
    return out_file_path