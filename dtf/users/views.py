# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

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

    def get_context_data(self, **kwargs):
        from utils.comments import latest_comments
        from courses.models import CourseFavourite
        from lessons.models import LessonFavourite
        from facebook_groups.models import FacebookGroup
        from profiles.models import UserProfile
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.get_object()
        feed = latest_comments(self.request)  # get latest comments
        paginator = Paginator(feed, 5)
        try:
            page = int(self.request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            feed = paginator.page(page)
        except (EmptyPage, InvalidPage):
            feed = paginator.page(paginator.num_pages)

        context['courses'] = CourseFavourite.objects.active(user)
        context['lessons'] = LessonFavourite.objects.active(user)
        context['groups'] = FacebookGroup.objects.purchased(user)
        context['comments'] = feed
        context['profile'] = UserProfile.objects.get_or_create(user=user)[0]
        return context


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
