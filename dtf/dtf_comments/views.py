from braces.views._ajax import JSONResponseMixin
from django.contrib.sites.models import Site
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from ipware.ip import get_real_ip, get_ip

from courses.models import Content
from dtf_comments.models import DTFComment
from dtf_comments.templatetags.markdown import markdown
from utils.views import (CreateFormBaseView, AjaxResponsePermissionMixin,
                         PermissionMixin)
from dtf_comments.forms import DTFCommentShareForm
from django_comments.views.moderation import perform_delete
from django_comments.views.utils import next_redirect
from django import template


class CommentDeleteView(PermissionMixin, View):
    decorators = {'GET': login_required, 'POST': login_required}

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(DTFComment, pk=self.kwargs['comment_id'],
                                    site__pk=settings.SITE_ID)
        next_url = request.GET.get('next', None)
        return render_to_response('comments/delete.html',
                                  {'comment': comment, 'next': next_url},
                                  template.RequestContext(request))

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(DTFComment, pk=self.kwargs['comment_id'],
                                    site__pk=settings.SITE_ID)
        if request.user.is_staff:
            perform_delete(request, comment)
        elif request.user == comment.user:
            comment.is_removed = True
            comment.save()
        return next_redirect(request, fallback=next or 'comments-delete-done',
                             c=comment.pk)


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

    def get_form_kwargs(self):
        kwargs = super(DTFCommentShareView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

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
