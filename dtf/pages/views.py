from django.views.decorators.csrf import csrf_exempt
from django.core.mail import mail_admins
from django.views.generic.base import TemplateView
from jsonview.decorators import json_view
from .forms import ContactForm, EmailForm
from django.shortcuts import render, get_object_or_404
from utils.search import EsClient


class PageView(TemplateView):
    template_name = "404.html"

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context['email_form'] = EmailForm()
        context['contact_form'] = ContactForm()
        return context


class HMHPageView(PageView):
    template_name = "pages/hmh/hmh_video.html"

    def get_template_names(self):
        '''
        Looks for a custom_template value and prepends it to template_names 
        if it exists otherwise 'nupages/page_detail.html' is used
        '''
        template_names = super(HMHPageView, self).get_template_names()
        code = self.request.GET.get('access_code', None)
        if code:
            video_id = str(code)[-1:]
            video_template_name = "pages/hmh/hmh_video_{}.html".format(video_id)
            template_names.insert(0, video_template_name)
        return template_names


class PublicCoursePageView(PageView):
    template_name = "courses/public_page.html"

    def get_context_data(self, **kwargs):
        from courses.models import Course
        from lessons.models import Lesson
        context = super(PublicCoursePageView, self).get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        context['course'] = course
        public_lessons = Lesson.objects.public(course=course)
        if len(public_lessons):
            context['lesson'] = public_lessons[0]
            print public_lessons
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


def search(request):
    res_list = []
    query = request.GET.get('query', None)
    if query:
        res_list = EsClient().search(query)
    return render(request, 'pages/search_results.html',
                  {'result_list': res_list})
