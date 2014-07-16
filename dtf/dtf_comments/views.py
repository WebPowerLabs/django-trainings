from braces.views._ajax import JSONResponseMixin
from django.contrib.sites.models import Site
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from ipware.ip import get_real_ip, get_ip

from courses.models import Content
from dtf_comments.models import DTFComment
from dtf_comments.templatetags.markdown import markdown
from utils.views import CreateFormBaseView, AjaxResponsePermissionMixin
from dtf_comments.forms import DTFCommentShareForm


class CommentPreviewView(AjaxResponsePermissionMixin, View):
    decorators = {'POST': login_required}

    def post_ajax(self, request, *args, **kwargs):
        data = request.POST.get('data', None)
        html = '<p>Nothing to preview.</p>'
        if data:
            html = markdown(data)
        return HttpResponse(html)


class DTFCommentShareView(AjaxResponsePermissionMixin, JSONResponseMixin,
                          CreateFormBaseView):
    decorators = {'GET': login_required, 'POST': login_required}
    model = DTFComment
    form_class = DTFCommentShareForm
    template_name = 'includes/share_form.html'

    def form_valid(self, form):
        content = get_object_or_404(Content, pk=self.kwargs['content_pk'])
        ip = get_real_ip(self.request)
        if not ip:
            ip = get_ip(self.request)
        self.object = form.save(commit=False)
        self.object.content_object = form.cleaned_data['object_pk']
        self.object.site = Site.objects.get(pk=settings.SITE_ID)
        self.object.hero_unit = content
        self.object.user = self.request.user
        self.object.user_name = self.request.user.username
        self.object.user_email = self.request.user.email
        self.object.ip_address = ip
        self.object.save()
        resp = self.render_json_response({'success': True})
        resp.status_code = 201
        return resp
