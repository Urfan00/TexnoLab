from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from .forms import CourseFeedbackForm
from .models import Course, CourseCategory, CourseFeedback, CourseProgram, CourseStatistic, CourseStudent, Gallery
from django.core.exceptions import ObjectDoesNotExist



class CourseListView(ListView):
    model = Course
    template_name = 'courses-list-5.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_category"] = CourseCategory.objects.filter(is_delete=False).all()
        context["courses"] = Course.objects.filter(is_delete=False, category__is_delete=False).all()
        return context


class CourseDetailView(DetailView, CreateView):
    model = Course
    form_class = CourseFeedbackForm
    template_name = 'courses-single-5.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            course_stats = CourseStatistic.objects.get(course=self.object)
            course_stats.read_count += 1
            course_stats.save()
        except ObjectDoesNotExist:
            # Create a new CourseStatistic object if it doesn't exist
            CourseStatistic.objects.create(course=self.object, read_count=1)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_programs'] = CourseProgram.objects.filter(is_delete=False, course__slug=self.kwargs.get('slug')).all()
        context['related_course'] = Course.objects.filter(is_delete=False, category = self.object.category).exclude(slug=self.kwargs.get('slug'))[:8]
        context['reviews'] = CourseFeedback.objects.filter(is_delete=False, course__slug = self.kwargs.get('slug')).all()
        context['galleries'] = Gallery.objects.filter(is_delete=False, course__slug=self.kwargs.get('slug')).all() # RZA GALLERY EKRANA CIXARMAQ
        context['user_review'] = CourseStudent.objects.filter(course__slug=self.kwargs.get('slug'), is_active=True, student=self.request.user).first()
        return context

    def form_valid(self, form, *args, **kwargs):
        form.instance.student = self.request.user
        form.instance.course = Course.objects.get(slug=self.kwargs.get('slug'))
        form.instance.save()
        self.object = self.get_object()
        try:
            course = CourseStatistic.objects.get(course=self.object)
            course.review_count += 1
            course.save()
        except ObjectDoesNotExist:
            CourseStatistic.objects.create(course=self.object, review_count=1)
        return redirect("course", slug=self.kwargs.get('slug'))
