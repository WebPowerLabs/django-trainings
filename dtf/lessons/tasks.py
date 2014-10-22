import uuid
from config.celery import app
from utils.video import convert_video
from django.core.files import File
import os


@app.task()
def process_video(video_obj):
    from lessons.models import Video
    format_list = {"mp4": video_obj.mp4, "webm": video_obj.webm}
    base_name = os.path.basename(video_obj.orig.name).rsplit('.', 1)[0]
    video_obj.status = Video.CONVERTING
    video_obj.save()
    try:
        for vformat, field in format_list.items():
            print 'Converting to {}...'.format(vformat)
            converted = convert_video(video_obj.orig.file, vformat) 
            print 'Saving video object...'
            djangofile = File(converted)
            field.save(base_name + '_{}.{}'.format(uuid.uuid4().hex, vformat),
                       djangofile)
            converted.close()
        video_obj.save()
        print 'Done.'
        video_obj.status = Video.CONVERTED
        video_obj.save()
    except Exception, e:
        print e
        video_obj.status = Video.ERROR
        video_obj.save()
