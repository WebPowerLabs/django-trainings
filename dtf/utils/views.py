from django.views.generic.base import View
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic.list import (MultipleObjectMixin,
                                       MultipleObjectTemplateResponseMixin)
from django.http.response import Http404


class CreateFormBaseView(ModelFormMixin, MultipleObjectMixin, ProcessFormView,
                         MultipleObjectTemplateResponseMixin, View):
    object = None

    def list(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})

    def get(self, *args, **kwargs):
        self.list(*args, **kwargs)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            kwargs['form'] = form
        self.list(self.request, *self.args, **self.kwargs)
        return super(CreateFormBaseView, self).get_context_data(**kwargs)


class PermissionMixin(object):
    """
    Adds a certain decorator to a specific HTTP method.
    """
    decorators = {}
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        decorators = self.decorators.get(request.method, [])
        try:
            for decorator in list(decorators):
                handler = decorator(handler)
        except TypeError:
            handler = decorators(handler)
        return handler(request, *args, **kwargs)


class AjaxResponsePermissionMixin(object):
    """
    Mixin allows you to define alternative methods for ajax requests. And
    adds a certain decorator to a specific HTTP method.
    """
    decorators = {}
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax() and request.method.lower() in self.http_method_names:
            handler = getattr(self, u"{0}_ajax".format(request.method.lower()),
                              self.http_method_not_allowed)
            self.request = request
            self.args = args
            self.kwargs = kwargs
        decorators = self.decorators.get(request.method, [])
        try:
            for decorator in list(decorators):
                handler = decorator(handler)
        except TypeError:
            handler = decorators(handler)
        return handler(request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def put_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)