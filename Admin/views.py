from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from Account.models import Account
from Blog.models import Blog
from Course.models import Course
from Service.models import Service
from django.db.models import Count


def page2(request):
    return render(request, 'dshb-courses.html')

def page3(request):
    return render(request, 'dshb-listing.html')



class DashboardView(ListView):
    model = Account
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_count'] = Account.objects.count()
        context['blog_count'] = Blog.objects.count()
        context['course_count'] = Course.objects.count()
        context['service_count'] = Service.objects.count()
        context["courses"] = Course.objects.annotate(review_count=Count('course_feedback'), program_count=Count('course_program'), student_count=Count('student_course')).order_by('-created_at').all()[:5]
        context["blogs"] = Blog.objects.order_by('-created_at').all()[:5]
        context["services"] = Service.objects.order_by('-created_at').all()[:5]
        return context