from config.celery import app
from utils.video import convert_video
from django.core.files.storage import default_storage
from django.core.files import File
import os


@app.task()
def process_video(video_obj):
    from lessons.models import Video
    format_list = {"mp4": video_obj.mp4, "webm": video_obj.webm}
    orig_file_path = video_obj.orig.path
    base_name = os.path.basename(orig_file_path).split('.')[:-1][0]
    video_obj.status = Video.CONVERTING
    video_obj.save()
    try:
        for k, v in format_list.items():
            print 'Converting to {}...'.format(k)
            converted_file_path = convert_video(orig_file_path, k) 
            print 'Saving video object...'
            file_obj = default_storage.open(converted_file_path)
            djangofile = File(file_obj)
            v.save(base_name + '.{}'.format(k), djangofile)
            file_obj.close()
            video_obj.save()
        print 'Done.'
        video_obj.status = Video.CONVERTED
        video_obj.save()
    except Exception, e:
        print e
        video_obj.status = Video.ERROR
        video_obj.save()