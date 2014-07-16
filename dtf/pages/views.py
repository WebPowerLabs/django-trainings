from django.views.decorators.csrf import csrf_exempt
from django.core.mail import mail_admins
from django.views.generic.base import TemplateView
from jsonview.decorators import json_view
from .forms import ContactForm, EmailForm


class PageView(TemplateView):

    template_name = "404.html"

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context['email_form'] = EmailForm()
        context['contact_form'] = ContactForm()
        return context


@csrf_exempt
@json_view
def contact(request):
    form = ContactForm(request.POST or None)
    context = {'success': False,
               'message': 'Please input subject and valid email address!'}
    if request.POST and form.is_valid():
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        feedback = form.cleaned_data['feedback']
        message = '{0} from {1}'.format(feedback, email)

        if feedback:
            subject = unicode('Feedback: {}').format(subject)
            context['message'] = 'Thanks for the feedback!'
        else:
            subject = unicode('Subscriber: {}').format(subject)
            context['message'] = 'Thanks for subscribing!'
        mail_admins(subject, message)
        context['success'] = True
    return context
