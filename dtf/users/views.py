# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import UserForm

# Import the customized User model
from .models import User
from django.views.generic.base import TemplateView
from allauth.account.views import LoginView


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by pk
    slug_field = "pk"
    slug_url_kwarg = "pk"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
            kwargs={"pk": self.request.user.pk})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                    kwargs={"pk": self.request.user.pk})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(pk=self.request.user.pk)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by pk
    slug_field = "pk"
    slug_url_kwarg = "pk"


class LoginCustomView(LoginView):
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['login'])
                self.request.session['account_user'] = user.pk
            except User.DoesNotExist:
                pass
        return LoginView.post(self, request, *args, **kwargs)


class EmailVerificationSentView(TemplateView):
    template_name = 'account/verification_sent.html'

    def get_context_data(self, **kwargs):
        try:
            email = User.objects.get(pk=self.request.session['account_user']
                                     ).email
        except User.DoesNotExist:
            email = ''
        kwargs['email'] = email
        return TemplateView.get_context_data(self, **kwargs)
