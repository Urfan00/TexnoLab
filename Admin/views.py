from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from Account.models import Account
from Admin.forms import CourseEditForm
from Blog.models import Blog
from Course.models import Course
from Service.models import Service
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy



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


class AdminCourseListView(ListView):
    model = Course
    template_name = 'course/dshb-courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        a_query = self.request.GET.get('a', '')
        d_query = self.request.GET.get('d', '')

        # Filter active courses
        active_courses = Course.objects.filter(
            Q(start_date__lte=today) & Q(end_date__gte=today)
        ).order_by('-start_date')
        
        # Filter inactive courses
        deactive_courses = Course.objects.exclude(
            Q(start_date__lte=today) & Q(end_date__gte=today)
        )

        # Apply search filter if a query is provided
        if a_query:
            active_courses = active_courses.filter(title__icontains=a_query)
        elif d_query:
            deactive_courses = deactive_courses.filter(title__icontains=d_query)

        context["active_course"] = active_courses
        context["deactive_course"] = deactive_courses


        return context


class AdminCourseEditView(CreateView):
    model = Course
    template_name = 'course/dshb-listing.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('slug')  # Get the course ID from URL kwargs
        course = get_object_or_404(Course, slug=course_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = CourseEditForm(instance=course)
        return render(request, 'dshb-listing.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CourseEditForm(request.POST, request.FILES, instance=get_object_or_404(Course, slug=kwargs.get('slug')))

        if form.is_valid():
            course = Course.objects.get(slug=kwargs.get('slug'))
            course.title = form.cleaned_data.get('title')
            course.description = form.cleaned_data.get('description')
            course.main_photo = form.cleaned_data.get('main_photo')
            course.video_link = form.cleaned_data.get('video_link')
            course.start_date = form.cleaned_data.get('start_date')
            course.end_date = form.cleaned_data.get('end_date')
            course.category = form.cleaned_data.get('category')
            course.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('course_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('course_dashboard')


class AdminCourseAddView(CreateView):
    model = Course
    template_name = 'course/dshb-listing-add.html'
    form_class = CourseEditForm
    success_url = reverse_lazy('course_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)

