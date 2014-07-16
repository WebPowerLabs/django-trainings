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


# def contact(request):
#     form = ContactForm()
#     if request.POST:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             email = form.cleaned_data['email']
#             message = '{} from {}'.format(form.cleaned_data['feedback'], email)
#             subject = unicode('Feedback: {}').format(subject)
#             mail_admins(subject, message)
#             _next = request.POST.get('next')
#             messages.success(request, 'Thanks for the feedback!')
#             if _next:
#                 return HttpResponseRedirect(_next)
#
#     _next = ""
#     if request.GET.get('next'):
#         _next = request.GET.get('next')
#
#     context = {'form': form, 'next': _next}
#     return render_to_response('pages/contact.html',
#         context,
#         context_instance=RequestContext(request))


@csrf_exempt
@json_view
def contact(request):
    context = {}
    if request.POST:
        if request.POST.get('email'):

            subject = request.POST.get('subject')
            email = request.POST.get('email')
            message = '{} from {}'.format(request.POST.get('feedback'), email)

            if request.POST.get('feedback'):
                subject = unicode('Feedback: {}').format(subject)
                context['message'] = 'Thanks for the feedback!'
            else:
                subject = unicode('Subscriber: {}').format(subject)
                context['message'] = 'Thanks for subscribing!'
            mail_admins(subject, message)
            context['success'] = True
        else:
            context['success'] = False
            context['message'] = 'Please input your email'
    return context
