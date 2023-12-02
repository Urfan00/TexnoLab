from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from .forms import CourseFeedbackForm, RequestUsForm
from .models import Course, CourseCategory, CourseFeedback, CourseProgram, CourseStatistic, CourseStudent, Gallery
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View



class CourseListView(ListView):
    model = Course
    template_name = 'courses-list-5.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_category"] = CourseCategory.objects.filter(is_delete=False).all()
        context["courses"] = Course.objects.filter(status=True, is_delete=False, category__is_delete=False).order_by('-start_date').all()
        return context


class CourseDetailView(View):
    template_name = 'courses-single-5.html'

    def get_object(self, queryset=None):
        # Retrieve the Course object based on the slug in the URL
        return Course.objects.get(slug=self.kwargs['slug'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            course_stats = CourseStatistic.objects.get(course=self.object)
            course_stats.read_count += 1
            course_stats.save()
        except ObjectDoesNotExist:
            # Create a new CourseStatistic object if it doesn't exist
            CourseStatistic.objects.create(course=self.object, read_count=1)

        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}
        context['course'] = self.get_object()
        context['course_programs'] = CourseProgram.objects.filter(is_delete=False, course__slug=self.kwargs.get('slug')).all()
        context['related_course'] = Course.objects.filter(is_delete=False, category=self.object.category).exclude(slug=self.kwargs.get('slug'))[:8]
        context['reviews'] = CourseFeedback.objects.filter(is_delete=False, course__slug=self.kwargs.get('slug')).all()
        context['galleries'] = Gallery.objects.filter(is_delete=False, course__slug=self.kwargs.get('slug')).all()

        if self.request.user.is_authenticated:
            context['user_review'] = CourseStudent.objects.filter(course__slug=self.kwargs.get('slug'), is_active=True, student=self.request.user).first()

        context['feedback_form'] = CourseFeedbackForm()
        context['request_form'] = RequestUsForm(initial={'course': self.object})

        return context

    def post(self, request, *args, **kwargs):
        try:
            course = CourseStatistic.objects.get(course=self.get_object())
            course.review_count += 1
            course.save()
        except ObjectDoesNotExist:
            CourseStatistic.objects.create(course=self.get_object(), review_count=1)

        # Process the feedback form
        feedback_form = CourseFeedbackForm(request.POST)
        request_form = RequestUsForm(request.POST)
        if request_form.is_valid():
            request_form.save()
            messages.success(request, 'Müraciətiniz uğurla edildi')
            return redirect("course", slug=self.kwargs.get('slug'))
        elif feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.course = self.get_object()
            feedback.student = request.user
            feedback.save()
            messages.success(request, 'Məlumatlarınız uğurla əlavə edildi')
            return redirect("course", slug=self.kwargs.get('slug'))
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect("course", slug=self.kwargs.get('slug'))
