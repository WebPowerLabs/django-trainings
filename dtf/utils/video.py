import os
from datetime import datetime
from subprocess import Popen
from django.core.files.storage import default_storage
import errno


def prepare_folders(full_path):
    directory = os.path.dirname(full_path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    if not os.path.isdir(directory):
        raise IOError("%s exists and is not a directory." % directory)


def convert_video(file_path, format):
    """
    Receives path to the video file and format in which it should be converted.
    Returns path to converted file.
    """
    if format not in ['webm', 'mp4']:
        raise ValueError('Argument "format" value must be "webm" or "mp4".')
    base_name = os.path.basename(file_path)
    
    tmp_path = r'tmp/{}{}.{}'.format(datetime.now().strftime('%Y/%m/%d/'),
                                  base_name, format)
    available_name = default_storage.get_available_name(tmp_path)
    
    out_file_path = default_storage.path(available_name)
    in_file_path = default_storage.path(file_path)
    prepare_folders(out_file_path)
    mp4_cmd = ['ffmpeg', '-i', in_file_path, '-b:v', '1500k', '-codec:v',
               'libx264', out_file_path]
    
    webm_cmd = ['ffmpeg', '-i', in_file_path, '-b:v', '1500k', '-codec:v',
                'libvpx', '-codec:a', 'libvorbis', '-b:a', '160000', '-f',
                'webm', '-g', '30', out_file_path]
    
    command = {'mp4': mp4_cmd, 'webm': webm_cmd}
    pipe = Popen(command[format])
    pipe.wait()
    return out_file_path


