from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import View
from braces.views._ajax import AjaxResponseMixin, JSONResponseMixin
from lessons.models import Lesson
from courses.models import Course
from profiles.models import Favourite


class FavouriteAddView(AjaxResponseMixin, JSONResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        model_map = {'lesson': Lesson,
                     'course': Course}
        model = model_map[self.kwargs['model_name']]
        obj = model.objects.get(pk=self.kwargs['pk'])
        ctype = ContentType.objects.get_for_model(model)
        Favourite.objects.get_or_create(content_type=ctype, object_id=obj.pk, user=self.request.user)
        return self.render_json_response({'success': True})
