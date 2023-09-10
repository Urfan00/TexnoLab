from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Course, CourseCategory, CourseProgram



class CourseListView(ListView):
    model = Course
    template_name = 'courses-list-5.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_category"] = CourseCategory.objects.all()
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses-single-5.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_programs'] = CourseProgram.objects.filter(sub_program_name__isnull=True).all()
        context['related_course'] = Course.objects.filter(category = self.object.category).exclude(slug=self.kwargs.get('slug'))[:8]
        return context


