from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from .forms import CourseFeedbackForm, RequestUsForm
from .models import Course, CourseCategory, CourseFeedback, CourseProgram, CourseStatistic, CourseVideo, Gallery
from ExamResult.models import CourseStudent
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CourseListView(ListView):
    model = Course
    template_name = 'courses-list-5.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = Course.objects.filter(status=True, is_delete=False, category__is_delete=False).order_by('-created_at').all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_category"] = CourseCategory.objects.filter(is_delete=False).all()
        courses = self.get_queryset()

        # Pagination
        page = self.request.GET.get('page')
        paginator = Paginator(courses, self.paginate_by)

        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        context["courses"] = courses
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses-single-5.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        self.update_read_count(obj)
        return obj

    def update_read_count(self, course):
        course_stats, created = CourseStatistic.objects.get_or_create(course=course)
        course_stats.read_count += 1
        course_stats.save()

    def update_review_count(self, course):
        course_stats, created = CourseStatistic.objects.get_or_create(course=course)
        course_stats.review_count += 1
        course_stats.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_programs'] = CourseProgram.objects.filter(is_delete=False, course__slug=self.get_object().slug).all()
        context['related_course'] = Course.objects.filter(is_delete=False, category=self.get_object().category).exclude(slug=self.get_object().slug)[:8]
        context['reviews'] = CourseFeedback.objects.filter(is_delete=False, course__slug=self.get_object().slug).all()
        context['galleries'] = Gallery.objects.filter(course__slug=self.get_object().slug).all()
        context['videos'] = CourseVideo.objects.filter(course__slug=self.get_object().slug).all()

        if self.request.user.is_authenticated:
            context['user_review'] = CourseStudent.objects.filter(course__slug=self.get_object().slug, student=self.request.user).first()
        context['feedback_form'] = CourseFeedbackForm()
        context['request_form'] = RequestUsForm(initial={'course': self.get_object()})

        return context

    def post(self, request, *args, **kwargs):
        try:
            self.update_review_count(self.get_object())
        except ObjectDoesNotExist:
            CourseStatistic.objects.create(course=self.get_object(), review_count=1)

        # Process the feedback form
        feedback_form = CourseFeedbackForm(request.POST)
        request_form = RequestUsForm(request.POST)
        if request_form.is_valid():
            request_form.save()
            messages.success(request, 'Müraciətiniz uğurla edildi')
            return redirect("course", slug=self.get_object().slug)
        elif feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.course = self.get_object()
            feedback.student = request.user
            feedback.save()
            messages.success(request, 'Məlumatlarınız uğurla əlavə edildi')
            return redirect("course", slug=self.get_object().slug)
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect("course", slug=self.get_object().slug)
