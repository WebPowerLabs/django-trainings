import tempfile
import subprocess


def convert_video(in_file, vformat):
    """
    Receives video file object and format in which it should be converted.
    Returns converted video file object.
    """
    if format not in ['webm', 'mp4']:
        raise ValueError('Argument "format" value must be "webm" or "mp4".')
    
    f_out = tempfile.NamedTemporaryFile(suffix=".{}".format(vformat))
    tmp_output_video = f_out.name

    mp4_cmd = 'ffmpeg -y -i - -b:v 1500k -codec:v libx264 {}'.format(
                                                             tmp_output_video)
    
    webm_cmd = 'ffmpeg -y -i - -b:v 1500k -codec:v libvpx -codec:a libvorbis \
                 -b:a 160000 -f webm -g 30 {}'.format(tmp_output_video)
    
    command = {'mp4': mp4_cmd, 'webm': webm_cmd}
    
    in_file.seek(0)
    subprocess.call(command[vformat], stdin=in_file, shell=True)
     
    return f_out