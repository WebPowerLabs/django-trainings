import tempfile
import subprocess
import os

def convert_video(in_file, vformat):
    """
    Receives video file object and format in which it should be converted.
    Returns converted video file object.
    """
    if vformat not in ['webm', 'mp4']:
        raise ValueError('Argument "format" value must be "webm" or "mp4".')
    
    f_in = tempfile.NamedTemporaryFile(delete=False)
    f_out = tempfile.NamedTemporaryFile(suffix=".{}".format(vformat))
    in_file.seek(0)
    f_in.write(in_file.read())
    f_in.close()
    tmp_input_video = f_in.name
    tmp_output_video = f_out.name

    mp4_cmd = 'ffmpeg -y -i {} -b:v 1500k -codec:v libx264 {}'.format(
                                                            tmp_input_video,
                                                            tmp_output_video)
    
    webm_cmd = 'ffmpeg -y -i {} -b:v 1500k -codec:v libvpx -codec:a libvorbis \
                -b:a 160000 -f webm -g 30 {}'.format(tmp_input_video,
                                                     tmp_output_video)
    
    command = {'mp4': mp4_cmd, 'webm': webm_cmd}
    
    subprocess.call(command[vformat], shell=True)
    os.remove(tmp_input_video)
    return f_out
