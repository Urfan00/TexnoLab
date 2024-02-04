from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from Account.models import Account
from Exam.models import Answer, CourseTopic, CourseTopicsTest, Question
from ExamResult.models import Group, CourseStudent, MentorLabEvaluation, StudentResult, TeacherEvaluation
from Core.forms import CertificateEditForm
from Core.models import FAQ, AboutUs, Certificate, ContactInfo, ContactUs, HomePageSliderTextIMG, Partner, Subscribe
from Blog.models import Blog, BlogCategory
from Course.models import Course, CourseCategory, CourseFeedback, CourseProgram, CourseStatistic, CourseVideo, Gallery, RequestUs, TeacherCourse
from Service.models import AllGalery, AllVideoGallery, Service, ServiceHome, ServiceImage, ServiceVideo
from TIM.models import TIM, TIMImage, TIMVideo
from services.mixins import AuthStudentPageMixin, AuthSuperUserCoordinatorMixin, AuthSuperUserCoordinatorTeacherMixin
from .forms import (AboutUsEditForm,
                    AccountEditForm,
                    AllGaleryEditForm,
                    AllVideoGalleryEditForm,
                    BlogCategoryEditForm,
                    BlogEditForm,
                    ContactInfoEditForm,
                    CourseCategoryEditForm,
                    CourseEditForm,
                    CourseProgramEditForm,
                    CourseStudentEditForm,
                    CourseTopicEditForm,
                    CourseTopicTestEditForm,
                    CourseVideoEditForm,
                    FAQEditForm,
                    GalLeryEditForm,
                    GroupEditForm,
                    HomePageSliderTextIMGForm,
                    PartnerEditForm,
                    RequestUsAdminCommentForm,
                    ServiceEditForm,
                    ServiceHomeEditForm,
                    ServiceImageEditForm,
                    ServiceVideoEditForm,
                    StaffAccountEditForm,
                    TIMEditForm,
                    TIMImageEditForm,
                    TIMVideoEditForm)
from django.db.models import Count, Sum, Avg, Max
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.db.models import F

# **********************************************************************************


# **********************************************************************************


class StudentDashboard(AuthStudentPageMixin, ListView):
    model = Account
    template_name = 'student-dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_point'] = TeacherEvaluation.objects.filter(student=self.request.user).aggregate(Sum('point'))['point__sum'] or 0
        context['lab_point'] = MentorLabEvaluation.objects.filter(student=self.request.user).aggregate(Sum('point'))['point__sum'] or 0

        average_total_point = StudentResult.objects.filter(student=self.request.user).values('exam_topics').annotate(
            max_total_point=Max('total_point')
            ).aggregate(
                Avg('max_total_point')
                )['max_total_point__avg'] or 0

        context['average_total_point'] = average_total_point * 5

        context["results"] = StudentResult.objects.filter(student=self.request.user).annotate(
            percent_point = F('total_point') * 5
        ).order_by('-created_at').all()

        student_results = StudentResult.objects.filter(student=self.request.user)
        labels = [result.exam_topics.topic_title for result in student_results]
        data = [result.total_point * 5 for result in student_results]

        context['labels'] = labels
        context['chart_data'] = {
            'labels': labels,
            'data': data,
        }

        return context


class DashboardView(AuthSuperUserCoordinatorMixin, ListView):
    model = Account
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_count'] = Account.objects.filter(is_active=True, is_staff=False, is_superuser=False).count()
        context['blog_count'] = Blog.objects.filter(blog_category__is_delete=False, is_delete=False, status=True).count()
        context['course_count'] = Course.objects.filter(category__is_delete=False, is_delete=False, status=True).count()
        context['service_count'] = ServiceHome.objects.filter(is_delete=False, status=True).count()
        context["courses"] = Course.objects.filter(category__is_delete=False, is_delete=False, status=True).annotate(
                review_count=Count('course_feedback__id', distinct=True),
                student_count=Count('course_group__student_group__id', distinct=True),
                program_count=Count('course_program__id', distinct=True)
            ).order_by('-created_at').all()[:5]
        context["blogs"] = Blog.objects.filter(blog_category__is_delete=False, is_delete=False, status=True).order_by('-created_at').all()[:5]
        context["services"] = ServiceHome.objects.filter(is_delete=False, status=True).order_by('-created_at').all()[:5]
        return context

# *************************************************************************************

# COURSE & COURSE CATEGORY
class AdminCourseListView(AuthSuperUserCoordinatorMixin, ListView):
    model = Course
    template_name = 'course/dshb-courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a_query = self.request.GET.get('a', '')
        d_query = self.request.GET.get('d', '')
        sc_query = self.request.GET.get('sc', '')
        k_query = self.request.GET.get('k', '')
        sk_query = self.request.GET.get('sk', '')
        p_query = self.request.GET.get('p', '')
        sp_query = self.request.GET.get('sp', '')

        # Filter active courses
        active_courses = Course.objects.filter(status=True, is_delete=False).order_by('-created_at')

        # Filter inactive courses
        deactive_courses = Course.objects.filter(status=False, is_delete=False).order_by('-created_at')

        delete_courses = Course.objects.filter(is_delete=True).order_by('-created_at')

        categories = CourseCategory.objects.filter(is_delete=False).order_by('-created_at')

        deleted_categories = CourseCategory.objects.filter(is_delete=True).order_by('-created_at')

        programs = CourseProgram.objects.filter(is_delete=False).all()
        d_programs = CourseProgram.objects.filter(is_delete=True).all()


        # Apply search filter if a query is provided
        if a_query:
            active_courses = active_courses.filter(title__icontains=a_query)
        elif d_query:
            deactive_courses = deactive_courses.filter(title__icontains=d_query)
        elif sc_query:
            delete_courses = delete_courses.filter(title__icontains=sc_query)
        elif k_query:
            categories = categories.filter(title__icontains=k_query)
        elif sk_query:
            deleted_categories = deleted_categories.filter(name__icontains=sk_query)
        elif p_query:
            programs = programs.filter(
                Q(course__title__icontains=p_query) | Q(program_name__icontains=p_query)
            )
        elif sp_query:
            d_programs = d_programs.filter(
                Q(course__title__icontains=sp_query) | Q(program_name__icontains=sp_query)
            )


        context["active_course"] = active_courses
        context["deactive_course"] = deactive_courses
        context["delete_course"] = delete_courses
        context["categories"] = categories
        context["deleted_categories"] = deleted_categories
        context["programs"] = programs
        context["d_programs"] = d_programs

        return context


# COURSE
class AdminCourseEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Course
    template_name = 'course/dshb-listing.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('slug')  # Get the course ID from URL kwargs
        course = get_object_or_404(Course, slug=course_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = CourseEditForm(instance=course)
        return render(request, 'course/dshb-listing.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CourseEditForm(request.POST, request.FILES, instance=get_object_or_404(Course, slug=kwargs.get('slug')))

        if form.is_valid():
            course = Course.objects.get(slug=kwargs.get('slug'))
            course.title = form.cleaned_data.get('title')
            course.description = form.cleaned_data.get('description')
            course.main_photo = form.cleaned_data.get('main_photo')
            course.video_link = form.cleaned_data.get('video_link')
            course.status = form.cleaned_data.get('status')
            course.category = form.cleaned_data.get('category')
            course.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('course_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('course_dashboard')


class AdminCourseAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Course
    template_name = 'course/dshb-listing-add.html'
    form_class = CourseEditForm
    success_url = reverse_lazy('course_dashboard')

    def form_valid(self, form):
        # Get the first CourseCategory instance
        first_category = CourseCategory.objects.first()

        # Set the category field of the Course instance to the first category
        form.instance.category = first_category
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminCourseDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        course.is_delete = True
        course.save()
        messages.success(request, 'Təlim uğurla silindi')
        return redirect('course_dashboard')


class AdminCourseUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        course.is_delete = False  # Set is_delete to False to undelete
        course.save()
        messages.success(request, 'Təlim uğurla bərpa olundu')
        return redirect('course_dashboard')


# COURSE CATEGORY
class AdminCourseCategoryEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = CourseCategory
    template_name = 'course/dshb-listing-course-category-edit.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        course = get_object_or_404(CourseCategory, pk=course_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = CourseCategoryEditForm(instance=course)
        return render(request, 'course/dshb-listing-course-category-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CourseCategoryEditForm(request.POST, instance=get_object_or_404(CourseCategory, pk=kwargs.get('pk')))

        if form.is_valid():
            course = CourseCategory.objects.get(pk=kwargs.get('pk'))
            course.name = form.cleaned_data.get('name')
            course.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('course_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('course_dashboard')


class AdminCourseCategoryAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = CourseCategory
    template_name = 'course/dshb-listing-course-category-add.html'
    form_class = CourseCategoryEditForm
    success_url = reverse_lazy('course_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminCourseCategoryDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(CourseCategory, pk=pk)
        course.is_delete = True
        course.save()
        messages.success(request, 'Təlim kateqoriyası uğurla silindi')
        return redirect('course_dashboard')


class AdminCourseCategoryUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(CourseCategory, pk=pk)
        course.is_delete = False  # Set is_delete to False to undelete
        course.save()
        messages.success(request, 'Təlim kateqoriyası uğurla bərpa olundu')
        return redirect('course_dashboard')


# Course Program
class AdminCourseProgramAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = CourseProgram
    template_name = 'course/dshb-listing-course-program-add.html'
    form_class = CourseProgramEditForm
    success_url = reverse_lazy('course_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminCourseProgramEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = CourseProgram
    template_name = 'course/dshb-listing-course-program-edit.html'

    def get(self, request, *args, **kwargs):
        program_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        program = get_object_or_404(CourseProgram, pk=program_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = CourseProgramEditForm(instance=program)
        return render(request, 'course/dshb-listing-course-program-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CourseProgramEditForm(request.POST, request.FILES, instance=get_object_or_404(CourseProgram, pk=kwargs.get('pk')))

        if form.is_valid():
            program = CourseProgram.objects.get(pk=kwargs.get('pk'))
            program.program_name = form.cleaned_data.get('program_name')
            program.description = form.cleaned_data.get('description')
            program.course = form.cleaned_data.get('course')
            program.file = form.cleaned_data.get('file')
            program.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('course_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('course_dashboard')


class AdminCourseProgramDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        program_id = kwargs.get('pk')
        program = get_object_or_404(CourseProgram, pk=program_id)
        program.is_delete = True
        program.save()
        messages.success(request, 'Təlim proqramı uğurla silindi')
        return redirect('course_dashboard')


class AdminCourseProgramUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        program = get_object_or_404(CourseProgram, pk=pk)
        program.is_delete = False  # Set is_delete to False to undelete
        program.save()
        messages.success(request, 'Təlim proqramı uğurla bərpa olundu')
        return redirect('course_dashboard')


# ********************************************************************************

# BLOG & BLOG CATEGORY
class AdminBlogListView(AuthSuperUserCoordinatorMixin, ListView):
    model = Blog
    template_name = 'blog/dshb-blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a_query = self.request.GET.get('a', '')
        d_query = self.request.GET.get('d', '')
        c_query = self.request.GET.get('c', '')
        sb_query = self.request.GET.get('sb', '')
        sc_query = self.request.GET.get('sc', '')

        # Filter active courses
        active_blog = Blog.objects.filter(status=True, is_delete=False).order_by('-created_at')
        
        # Filter inactive courses
        deactive_blog = Blog.objects.filter(status=False, is_delete=False).order_by('-created_at')

        category = BlogCategory.objects.filter(is_delete=False).order_by('-created_at').all()
        delete_category = BlogCategory.objects.filter(is_delete=True).order_by('-created_at').all()

        delete_blog = Blog.objects.filter(is_delete=True).order_by('-created_at')


        # Apply search filter if a query is provided
        if a_query:
            active_blog = active_blog.filter(title__icontains=a_query)
        elif d_query:
            deactive_blog = deactive_blog.filter(title__icontains=d_query)
        elif sb_query:
            delete_blog = delete_blog.filter(title__icontains=sb_query)
        elif c_query:
            category = category.filter(name__icontains=c_query)
        elif sc_query:
            delete_category = category.filter(name__icontains=sc_query)


        context["active_blogs"] = active_blog
        context["deactive_blogs"] = deactive_blog
        context["categories"] = category
        context["delete_blogs"] = delete_blog
        context["delete_category"] = delete_category

        return context


# BLOG
class AdminBlogAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Blog
    template_name = 'blog/dshb-listing-add-blog.html'
    form_class = BlogEditForm
    success_url = reverse_lazy('blog_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminBlogEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Blog
    template_name = 'blog/dshb-listing-blog.html'

    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get('slug')  # Get the course ID from URL kwargs
        blog = get_object_or_404(Blog, slug=blog_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = BlogEditForm(instance=blog)
        return render(request, 'blog/dshb-listing-blog.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = BlogEditForm(request.POST, request.FILES, instance=get_object_or_404(Blog, slug=kwargs.get('slug')))

        if form.is_valid():
            blog = Blog.objects.get(slug=kwargs.get('slug'))
            blog.title = form.cleaned_data.get('title')
            blog.description = form.cleaned_data.get('description')
            blog.photo = form.cleaned_data.get('photo')
            blog.date = form.cleaned_data.get('date')
            blog.status = form.cleaned_data.get('status')
            blog.blog_category = form.cleaned_data.get('blog_category')
            blog.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('blog_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('blog_dashboard')


class AdminBlogDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        blog_id = kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        blog.is_delete = True
        blog.save()
        messages.success(request, 'Bloq uğurla silindi')
        return redirect('blog_dashboard')


class AdminBlogUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        blog.is_delete = False  # Set is_delete to False to undelete
        blog.save()
        messages.success(request, 'Bloq uğurla bərpa olundu')
        return redirect('blog_dashboard')


# BLOG CATEGORY
class AdminBlogCategoryAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = BlogCategory
    template_name = 'blog/dshb-listing-add-blog-category.html'
    form_class = BlogCategoryEditForm
    success_url = reverse_lazy('blog_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminBlogCategoryEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = BlogCategory
    template_name = 'blog/dshb-listing-blog-category.html'

    def get(self, request, *args, **kwargs):
        blog_category_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        blog_category = get_object_or_404(BlogCategory, pk=blog_category_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = BlogCategoryEditForm(instance=blog_category)
        return render(request, 'blog/dshb-listing-blog-category.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = BlogCategoryEditForm(request.POST, instance=get_object_or_404(BlogCategory, pk=kwargs.get('pk')))

        if form.is_valid():
            blog_category = BlogCategory.objects.get(pk=kwargs.get('pk'))
            blog_category.name = form.cleaned_data.get('name')
            blog_category.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('blog_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('blog_dashboard')


class AdminBlogCategoryDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = get_object_or_404(BlogCategory, pk=category_id)
        category.is_delete = True
        category.save()
        messages.success(request, 'Bloq kateqoriyası uğurla silindi')
        return redirect('blog_dashboard')


class AdminBlogCategoryUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(BlogCategory, pk=pk)
        category.is_delete = False  # Set is_delete to False to undelete
        category.save()
        messages.success(request, 'Bloq kateqoriyası uğurla bərpa olundu')
        return redirect('blog_dashboard')

# ********************************************************************************


# Service & Service Home & Service Gallery
class AdminServiceListView(AuthSuperUserCoordinatorMixin, ListView):
    model = ServiceHome
    template_name = 'service/dshb-service.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a_query = self.request.GET.get('a', '')
        d_query = self.request.GET.get('d', '')
        sx_query = self.request.GET.get('sx', '')
        as_query = self.request.GET.get('as', '')
        ds_query = self.request.GET.get('ds', '')
        ss_query = self.request.GET.get('ss', '')
        g_query = self.request.GET.get('g', '')
        v_query = self.request.GET.get('v', '')

        active_service_home = ServiceHome.objects.filter(status=True, is_delete=False).order_by('-created_at')
        deactive_service_home = ServiceHome.objects.filter(status=False, is_delete=False).order_by('-created_at')
        delete_service_home = ServiceHome.objects.filter(is_delete=True).order_by('-created_at')

        active_service = Service.objects.filter(status=True, is_delete=False).order_by('-created_at')
        deactive_service = Service.objects.filter(status=False, is_delete=False).order_by('-created_at')
        delete_service = Service.objects.filter(is_delete=True).order_by('-created_at')

        galleries = ServiceImage.objects.filter(service__status=True, service__is_delete=False).all()
        videos = ServiceVideo.objects.filter(service__status=True, service__is_delete=False).all()

        if a_query:
            active_service_home = active_service_home.filter(title__icontains=a_query)
        elif d_query:
            deactive_service_home = deactive_service_home.filter(title__icontains=d_query)
        elif sx_query:
            delete_service_home = delete_service_home.filter(title__icontains=sx_query)
        elif as_query:
            delete_service_home = delete_service_home.filter(title__icontains=as_query)
        elif ds_query:
            delete_service_home = delete_service_home.filter(title__icontains=ds_query)
        elif ss_query:
            delete_service_home = delete_service_home.filter(title__icontains=ss_query)
        elif g_query:
            galleries = galleries.filter(service__title__icontains=g_query)
        elif v_query:
            videos = videos.filter(service__title__icontains=v_query)

        context["active_services_home"] = active_service_home
        context["deactive_services_home"] = deactive_service_home
        context["delete_services_home"] = delete_service_home

        context["active_services"] = active_service
        context["deactive_services"] = deactive_service
        context["delete_services"] = delete_service

        # Pagination
        page = self.request.GET.get('page')
        paginator = Paginator(galleries, self.paginate_by)

        try:
            galleries = paginator.page(page)
        except PageNotAnInteger:
            galleries = paginator.page(1)
        except EmptyPage:
            galleries = paginator.page(paginator.num_pages)

        context['galleries'] = galleries
        context['videos'] = videos

        return context


# Service
class AdminServiceAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Service
    template_name = 'service/dshb-listing-add-service.html'
    form_class = ServiceEditForm
    success_url = reverse_lazy('service_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminServiceEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Service
    template_name = 'service/dshb-service-edit.html'

    def get(self, request, pk, *args, **kwargs):
        service = get_object_or_404(Service, pk=pk)

        form = ServiceEditForm(instance=service)
        return render(request, 'service/dshb-service-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ServiceEditForm(request.POST, request.FILES, instance=get_object_or_404(Service, pk=kwargs.get('pk')))

        if form.is_valid():
            service = Service.objects.get(pk=kwargs.get('pk'))
            service.title = form.cleaned_data.get('title')
            service.description1 = form.cleaned_data.get('description1')
            service.description2 = form.cleaned_data.get('description2')
            service.status = form.cleaned_data.get('status')
            service.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('service_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('service_dashboard')


class AdminServiceDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        service = get_object_or_404(Service, pk=service_id)
        service.is_delete = True
        service.save()
        messages.success(request, 'Servis uğurla silindi')
        return redirect('service_dashboard')


class AdminServiceUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        service = get_object_or_404(Service, pk=pk)
        service.is_delete = False  # Set is_delete to False to undelete
        service.save()
        messages.success(request, 'Servis uğurla bərpa olundu')
        return redirect('service_dashboard')


class AdminServiceDetailView(AuthSuperUserCoordinatorMixin, DetailView):
    model = Service
    template_name = 'service/dshb-service-look.html'
    context_object_name = 'service'


# ********************************************************************************
# Service Home
class AdminServiceHomeAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = ServiceHome
    template_name = 'service/service-home/dshb-listing-add-service-home.html'
    form_class = ServiceHomeEditForm
    success_url = reverse_lazy('service_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminServiceHomeEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = ServiceHome
    template_name = 'service/service-home/dshb-listing-service-home.html'

    def get(self, request, pk, *args, **kwargs):
        service = get_object_or_404(ServiceHome, pk=pk)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = ServiceHomeEditForm(instance=service)
        return render(request, 'service/service-home/dshb-listing-service-home.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ServiceHomeEditForm(request.POST, request.FILES, instance=get_object_or_404(ServiceHome, pk=kwargs.get('pk')))

        if form.is_valid():
            service = ServiceHome.objects.get(pk=kwargs.get('pk'))
            service.title = form.cleaned_data.get('title')
            service.photo = form.cleaned_data.get('photo')
            service.status = form.cleaned_data.get('status')
            service.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('service_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('service_dashboard')


class AdminServiceHomeDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        service = get_object_or_404(ServiceHome, pk=service_id)
        service.is_delete = True
        service.save()
        messages.success(request, 'Xidmət uğurla silindi')
        return redirect('service_dashboard')


class AdminServiceHomeUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        service = get_object_or_404(ServiceHome, pk=pk)
        service.is_delete = False  # Set is_delete to False to undelete
        service.save()
        messages.success(request, 'Xidmət uğurla bərpa olundu')
        return redirect('service_dashboard')


# ********************************************************************************
# Service Gallery
class AdminServiceImageAddView(AuthSuperUserCoordinatorMixin, FormView):
    model = ServiceImage
    template_name = 'service/service-gallery/dshb-service-image-add.html'
    form_class = ServiceImageEditForm
    success_url = reverse_lazy('service_dashboard')

    def form_valid(self, form):
        # Get the selected course from the form
        selected_course = form.cleaned_data['service']

        uploaded_files = self.request.FILES.getlist('photo')

        for uploaded_file in uploaded_files:
            ServiceImage.objects.create(photo=uploaded_file, service=selected_course)

        messages.success(self.request, 'Şəkil uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Şəkil əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminServiceImageDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = ServiceImage.objects.get(pk=image_id)
            image.delete()
        except ServiceImage.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Şəkil uğurla silindi')

        return redirect('service_dashboard')


# ********************************************************************************
# Service Video
class AdminServiceVideoAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = ServiceVideo
    template_name = 'service/service-gallery/dshb-service-video-add.html'
    form_class = ServiceVideoEditForm
    success_url = reverse_lazy('service_dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Video uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Video əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminServiceVideoDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = ServiceVideo.objects.get(pk=image_id)
            image.delete()
        except ServiceVideo.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Video uğurla silindi')

        return redirect('service_dashboard')


# ********************************************************************************
# Course Statistic
class AdminCourseStatisticListView(AuthSuperUserCoordinatorMixin, ListView):
    model = CourseStatistic
    template_name = 'course/dshb-courses-statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ks_query = self.request.GET.get('ks', '')

        statistics = CourseStatistic.objects.order_by('-created_at').all()


        if ks_query:
            statistics = statistics.filter(course__title__icontains=ks_query)

        context["statistics"] = statistics

        return context

# ********************************************************************************
# Course Feedback
class AdminCourseFeedbackListView(AuthSuperUserCoordinatorMixin, ListView):
    model = CourseFeedback
    template_name = 'feedback/dshb-feedback.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        f_query = self.request.GET.get('f', '')
        df_query = self.request.GET.get('df', '')

        feedbacks = CourseFeedback.objects.filter(is_delete=False).order_by('-created_at').all()
        d_feedbacks = CourseFeedback.objects.filter(is_delete=True).order_by('-created_at').all()

        if f_query:
            feedbacks = feedbacks.filter(
                Q(course__title__icontains=f_query) | Q(student__first_name__icontains=f_query) | Q(student__last_name__icontains=f_query)
            )
        elif df_query:
            d_feedbacks = d_feedbacks.filter(
                Q(course__title__icontains=df_query) | Q(student__first_name__icontains=df_query) | Q(student__last_name__icontains=df_query)
            )

        context["feedbacks"] = feedbacks
        context["d_feedbacks"] = d_feedbacks

        return context


class AdminCourseFeedbackDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        feedback_id = kwargs.get('pk')
        feedback = get_object_or_404(CourseFeedback, pk=feedback_id)
        feedback.is_delete = True
        feedback.save()
        messages.success(request, 'Feedback uğurla silindi')
        return redirect('feedback_dashboard')


class AdminCourseFeedbackUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        feedback = get_object_or_404(CourseFeedback, pk=pk)
        feedback.is_delete = False  # Set is_delete to False to undelete
        feedback.save()
        messages.success(request, 'Feedback uğurla bərpa olundu')
        return redirect('feedback_dashboard')


class AdminCourseFeedbackDetailView(AuthSuperUserCoordinatorMixin, DetailView):
    model = CourseFeedback
    template_name = 'feedback/dshb-courses-feedback-look.html'
    context_object_name = 'feedback'


# ********************************************************************************
# Partner
class AdminPartnerListView(AuthSuperUserCoordinatorMixin, ListView):
    model = Partner
    template_name = 'partner/dshb-partner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_query = self.request.GET.get('p', '')
        sp_query = self.request.GET.get('sp', '')

        partners = Partner.objects.filter(is_delete=False).order_by('-created_at').all()
        d_partners = Partner.objects.filter(is_delete=True).order_by('-created_at').all()

        if p_query:
            partners = partners.filter(title__icontains=p_query)
        elif sp_query:
            d_partners = d_partners.filter(title__icontains=sp_query)

        context["partners"] = partners
        context["d_partners"] = d_partners

        return context


class AdminPartnerAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Partner
    template_name = 'partner/dshb-partner-add.html'
    form_class = PartnerEditForm
    success_url = reverse_lazy('partner_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminPartnerEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Partner
    template_name = 'partner/dshb-partner-edit.html'

    def get(self, request, *args, **kwargs):
        partner_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        partner = get_object_or_404(Partner, pk=partner_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = PartnerEditForm(instance=partner)
        return render(request, 'partner/dshb-partner-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PartnerEditForm(request.POST, request.FILES, instance=get_object_or_404(Partner, pk=kwargs.get('pk')))

        if form.is_valid():
            partner = Partner.objects.get(pk=kwargs.get('pk'))
            partner.title = form.cleaned_data.get('title')
            partner.img = form.cleaned_data.get('img')
            partner.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('partner_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('partner_dashboard')


class AdminPartnerDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        partner_id = kwargs.get('pk')
        partner = get_object_or_404(Partner, pk=partner_id)
        partner.is_delete = True
        partner.save()
        messages.success(request, 'Tərəfdaşlar uğurla silindi')
        return redirect('partner_dashboard')


class AdminPartnerUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        partner = get_object_or_404(Partner, pk=pk)
        partner.is_delete = False  # Set is_delete to False to undelete
        partner.save()
        messages.success(request, 'Tərəfdaşlar uğurla bərpa olundu')
        return redirect('partner_dashboard')


# ********************************************************************************
# FAQ
class AdminFAQListView(AuthSuperUserCoordinatorMixin, ListView):
    model = FAQ
    template_name = 'faq/dshb-faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faq_query = self.request.GET.get('faq', '')
        s_faq_query = self.request.GET.get('s_faq', '')

        faqs = FAQ.objects.filter(is_delete=False).order_by('-created_at').all()
        s_faqs = FAQ.objects.filter(is_delete=True).order_by('-created_at').all()

        if faq_query:
            faqs = faqs.filter(question__icontains=faq_query)
        elif s_faq_query:
            s_faqs = s_faqs.filter(question__icontains=s_faq_query)

        context["faqs"] = faqs
        context["s_faqs"] = s_faqs

        return context


class AdminFAQAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = FAQ
    template_name = 'faq/dshb-faq-add.html'
    form_class = FAQEditForm
    success_url = reverse_lazy('faq_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminFAQEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = FAQ
    template_name = 'faq/dshb-faq-edit.html'

    def get(self, request, *args, **kwargs):
        faq_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        faq = get_object_or_404(FAQ, pk=faq_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = FAQEditForm(instance=faq)
        return render(request, 'faq/dshb-faq-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = FAQEditForm(request.POST)

        if form.is_valid():
            faq = FAQ.objects.get(pk=kwargs.get('pk'))
            faq.question = form.cleaned_data.get('question')
            faq.answer = form.cleaned_data.get('answer')
            faq.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('faq_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('faq_dashboard')


class AdminFAQDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        faq_id = kwargs.get('pk')
        faq = get_object_or_404(FAQ, pk=faq_id)
        faq.is_delete = True
        faq.save()
        messages.success(request, 'FAQ uğurla silindi')
        return redirect('faq_dashboard')


class AdminFAQUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        faq = get_object_or_404(FAQ, pk=pk)
        faq.is_delete = False  # Set is_delete to False to undelete
        faq.save()
        messages.success(request, 'FAQ uğurla bərpa olundu')
        return redirect('faq_dashboard')


# ********************************************************************************
# Contact US & Request US
class AdminContactUSListView(AuthSuperUserCoordinatorMixin, ListView):
    model = ContactUs
    template_name = 'apply/dshb-apply.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cu_query = self.request.GET.get('cu', '')
        bcu_query = self.request.GET.get('bcu', '')
        dcu_query = self.request.GET.get('dcu', '')
        m_query = self.request.GET.get('m', '')
        bm_query = self.request.GET.get('bm', '')
        dr_query = self.request.GET.get('dr', '')

        contact_us = ContactUs.objects.filter(is_view=False, is_delete=False).order_by('-created_at').all()
        b_contact_us = ContactUs.objects.filter(is_view=True, is_delete=False).order_by('-created_at').all()
        d_contact_us = ContactUs.objects.filter(is_delete=True).order_by('-created_at').all()
        request_us = RequestUs.objects.filter(is_view=False, is_delete=False).order_by('-created_at').all()
        b_request_us = RequestUs.objects.filter(is_view=True, is_delete=False).order_by('-created_at').all()
        d_request_us = RequestUs.objects.filter(is_delete=True).order_by('-created_at').all()

        if cu_query:
            contact_us = contact_us.filter(Q(fullname__icontains=cu_query) | Q(email__icontains=cu_query))
        elif bcu_query:
            b_contact_us = b_contact_us.filter(Q(fullname__icontains=bcu_query) | Q(email__icontains=bcu_query))
        elif dcu_query:
            d_contact_us = d_contact_us.filter(Q(fullname__icontains=dcu_query) | Q(email__icontains=dcu_query))
        elif m_query:
            request_us = request_us.filter(
                Q(course__title__icontains=m_query) | Q(fullname__icontains=m_query)
            )
        elif bm_query:
            b_request_us = b_request_us.filter(
                Q(course__title__icontains=bm_query) | Q(fullname__icontains=bm_query)
            )
        elif dr_query:
            d_request_us = d_request_us.filter(
                Q(course__title__icontains=dr_query) | Q(fullname__icontains=dr_query)
            )

        context["contact_us"] = contact_us
        context["b_contact_us"] = b_contact_us
        context["d_contact_us"] = d_contact_us
        context["request_us"] = request_us
        context["b_request_us"] = b_request_us
        context["d_request_us"] = d_request_us

        return context


class AdminContactUsDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        contact_us_id = kwargs.get('pk')
        contact_us = get_object_or_404(ContactUs, pk=contact_us_id)
        contact_us.is_delete = True
        contact_us.save()
        messages.success(request, 'Bizimlə əlaqə uğurla silindi')
        return redirect('apply_dashboard')


class AdminContactUsUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        contact_us = get_object_or_404(ContactUs, pk=pk)
        contact_us.is_delete = False  # Set is_delete to False to undelete
        contact_us.save()
        messages.success(request, 'Bizimlə əlaqə uğurla bərpa olundu')
        return redirect('apply_dashboard')


class AdminContactUsView(AuthSuperUserCoordinatorMixin, DetailView):
    model = ContactUs
    template_name = 'apply/dshb-contact_us-look.html'
    context_object_name = 'contact_us'

    def get(self, request, *args, **kwargs):
        contact_us = ContactUs.objects.get(pk=self.get_object().pk)
        contact_us.is_view = True
        contact_us.save()
        return super().get(request, *args, **kwargs)


# Request US
class AdminRequestUsDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(RequestUs, pk=pk)
        course.is_delete = True
        course.save()
        messages.success(request, 'Təlim müraciəti uğurla silindi')
        return redirect('apply_dashboard')


class AdminRequestUsUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(RequestUs, pk=pk)
        course.is_delete = False  # Set is_delete to False to undelete
        course.save()
        messages.success(request, 'Təlim müraciəti uğurla bərpa olundu')
        return redirect('apply_dashboard')


class AdminRequestUsDetailView(AuthSuperUserCoordinatorMixin, DetailView, CreateView):
    model = RequestUs
    template_name = 'apply/dshb-courses-request-look.html'
    context_object_name = 'request'
    form_class = RequestUsAdminCommentForm

    def form_valid(self, form, *args, **kwargs):
        if form.is_valid():
            # Your code to save the admin_comment here
            request_us = RequestUs.objects.get(pk=self.get_object().pk)
            request_us.select_option = form.cleaned_data['select_option']
            if form.cleaned_data['admin_comment']:
                request_us.admin_comment = form.cleaned_data['admin_comment']
                request_us.is_view = True
            request_us.save()
            messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
            return redirect("request_us_look", pk=self.kwargs.get('pk'))
        else:
            messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
            return redirect("request_us_look", pk=self.kwargs.get('pk'))


# ********************************************************************************
# About Us & Contact Info & Home page text Img
class AdminAboutContactInfoListView(AuthSuperUserCoordinatorMixin, View):
    template_name = 'core/about_us-contact_us/dshb-about-contact-info.html'

    def get_context_data(self):
        context = {}
        context["about"] = AboutUs.objects.first()
        context["contact_info"] = ContactInfo.objects.first()
        context["slider"] = HomePageSliderTextIMG.objects.last()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {**self.get_context_data()})


class AdminAboutUsEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = AboutUs
    template_name = 'core/about_us-contact_us/dshb-about_us-edit.html'

    def get(self, request, *args, **kwargs):
        about = AboutUs.objects.first()

        form = AboutUsEditForm(instance=about)
        return render(request, 'core/about_us-contact_us/dshb-about_us-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AboutUsEditForm(request.POST, request.FILES, instance=AboutUs.objects.first())

        if form.is_valid():
            about = AboutUs.objects.first()
            about.title = form.cleaned_data.get('title')
            about.content = form.cleaned_data.get('content')
            about.img1 = form.cleaned_data.get('img1')
            # about.img2 = form.cleaned_data.get('img2')
            # about.img3 = form.cleaned_data.get('img3')
            about.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('about_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('about_dashboard')


class AdminContactInfoEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = ContactInfo
    template_name = 'core/about_us-contact_us/dshb-contact_info-edit.html'

    def get(self, request, *args, **kwargs):
        contact_info = ContactInfo.objects.first()

        form = ContactInfoEditForm(instance=contact_info)
        return render(request, 'core/about_us-contact_us/dshb-contact_info-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactInfoEditForm(request.POST)

        if form.is_valid():
            contact_info = ContactInfo.objects.first()
            contact_info.title = form.cleaned_data.get('title')
            contact_info.location = form.cleaned_data.get('location')
            contact_info.location_url = form.cleaned_data.get('location_url')
            contact_info.content = form.cleaned_data.get('content')
            contact_info.phone_number = form.cleaned_data.get('phone_number')
            contact_info.email = form.cleaned_data.get('email')
            contact_info.instagram = form.cleaned_data.get('instagram')
            contact_info.twitter = form.cleaned_data.get('twitter')
            contact_info.facebook = form.cleaned_data.get('facebook')
            contact_info.github = form.cleaned_data.get('github')
            contact_info.youtube = form.cleaned_data.get('youtube')
            contact_info.linkedIn = form.cleaned_data.get('linkedIn')
            contact_info.tiktok = form.cleaned_data.get('tiktok')
            contact_info.whatsapp = form.cleaned_data.get('whatsapp')
            contact_info.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('about_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('about_dashboard')


class AdminHomePageSliderTextIMGEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = HomePageSliderTextIMG
    template_name = 'core/home-page-slider/dshb-homepage-slider-edit.html'

    def get(self, request, *args, **kwargs):
        slider = HomePageSliderTextIMG.objects.last()

        form = HomePageSliderTextIMGForm(instance=slider)
        return render(request, 'core/home-page-slider/dshb-homepage-slider-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = HomePageSliderTextIMGForm(request.POST, request.FILES, instance=HomePageSliderTextIMG.objects.last())

        if form.is_valid():
            slider = HomePageSliderTextIMG.objects.last()
            slider.text = form.cleaned_data.get('text')
            slider.img = form.cleaned_data.get('img')
            slider.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('about_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('about_dashboard')


# Account & Register
class AdminAccountListView(AuthSuperUserCoordinatorMixin, ListView):
    model = Account
    template_name = 'account/dshb-account-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s_query = self.request.GET.get('s', '')
        cs_query = self.request.GET.get('cs', '')
        g_query = self.request.GET.get('g', '')
        k_query = self.request.GET.get('k', '')
        af_query = self.request.GET.get('af', '')
        df_query = self.request.GET.get('df', '')


        students = Account.objects.filter(is_staff=False, is_superuser=False, is_delete=False).order_by('-date_joined')
        c_students = CourseStudent.objects.filter(is_deleted=False, student__is_staff=False, student__is_superuser=False, student__is_delete=False).all()
        k_students = CourseStudent.objects.filter(is_keb=True, is_deleted=False, student__is_staff=False, student__is_superuser=False, student__is_delete=False).all()
        groups = Group.objects.all()
        allow_feedback = Account.objects.filter(
            is_delete=False,
            is_superuser=False,
            feedback_status=True
        ).filter(
            Q(feedback__isnull=False) & ~Q(feedback="")
        ).all()
        dont_allow_feedback = Account.objects.filter(
            is_delete=False,
            is_superuser=False,
            feedback_status=False
        ).filter(
            Q(feedback__isnull=False) & ~Q(feedback="")
        ).all()

        if s_query:
            students = students.filter(
                Q(first_name__icontains=s_query) | Q(last_name__icontains=s_query)
            )
        elif cs_query:
            c_students = c_students.filter(
                Q(student__first_name__icontains=cs_query) | Q(student__last_name__icontains=cs_query) | Q(group__name__icontains=cs_query) | Q(course__title__icontains=cs_query)
            )
        elif k_query:
            k_students = k_students.filter(
                Q(student__first_name__icontains=k_query) | Q(student__last_name__icontains=k_query) | Q(group__name__icontains=k_query) | Q(course__title__icontains=k_query)
            )
        elif g_query:
            groups = groups.filter(
                Q(name__icontains=g_query) | Q(name__icontains=g_query)
            )
        elif af_query:
            allow_feedback = allow_feedback.filter(
                Q(first_name__icontains=af_query) | Q(last_name__icontains=af_query)
            )
        elif df_query:
            dont_allow_feedback = dont_allow_feedback.filter(
                Q(first_name__icontains=df_query) | Q(last_name__icontains=df_query)
            )

        context["students"] = students
        context["c_students"] = c_students
        context["k_students"] = k_students
        context["groups"] = groups
        context["allow_feedback"] = allow_feedback
        context["dont_allow_feedback"] = dont_allow_feedback

        return context

    def post(self, request, *args, **kwargs):
        if 'selected_students' in request.POST:
            selected_student_ids = request.POST.get('selected_students').split(',')
            CourseStudent.objects.filter(id__in=selected_student_ids).update(is_active=True)
            return redirect('account_dashboard')

        return super().post(request, *args, **kwargs)


class AdminFEEDBACKDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        feedback = get_object_or_404(Account, pk=pk)
        feedback.feedback_status = False
        feedback.save()
        messages.success(request, 'Tələbənin rəyinin statusu uğurla dəyişildi.')
        return redirect('account_dashboard')


class AdminFEEDBACKUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        feedback = get_object_or_404(Account, pk=pk)
        feedback.feedback_status = True  # Set is_delete to False to undelete
        feedback.save()
        messages.success(request, 'Tələbənin rəyinin statusu uğurla dəyişildi.')
        return redirect('account_dashboard')


class AdminKEBDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        keb = get_object_or_404(CourseStudent, pk=pk)
        keb.is_keb = False
        keb.save()
        messages.success(request, 'Məzun uğurla kadr ehtiyat bazasından silindi')
        return redirect('account_dashboard')


class AdminKEBUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        keb = get_object_or_404(CourseStudent, pk=pk)
        keb.is_keb = True  # Set is_delete to False to undelete
        keb.save()
        messages.success(request, 'Məzun uğurla kadr ehtiyat bazasına əlavə olundu')
        return redirect('account_dashboard')


class AdminAccountDetailView(AuthSuperUserCoordinatorMixin, DetailView):
    model = Account
    template_name = 'account/dshb-account-look.html'
    context_object_name = 'student'


class AdminAccountAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Account
    template_name = 'account/dshb-account-add.html'
    form_class = AccountEditForm
    success_url = reverse_lazy('account_dashboard')

    def form_valid(self, form):
        fin = form.cleaned_data['FIN']
        form.instance.password = make_password(fin)
        form.instance.staff_status = 'Tələbə'
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminAccountEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Account
    template_name = 'account/dshb-account-edit.html'

    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        account = get_object_or_404(Account, pk=account_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = AccountEditForm(instance=account)
        return render(request, 'account/dshb-account-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AccountEditForm(request.POST, request.FILES, instance=get_object_or_404(Account, pk=kwargs.get('pk')))

        if form.is_valid():
            account = Account.objects.get(pk=kwargs.get('pk'))
            account.first_name = form.cleaned_data.get('first_name')
            account.last_name = form.cleaned_data.get('last_name')
            account.FIN = form.cleaned_data.get('FIN')
            account.birthday = form.cleaned_data.get('birthday')
            account.id_code = form.cleaned_data.get('id_code')
            account.balance = form.cleaned_data.get('balance')
            account.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('account_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('account_dashboard')


# Group
class AdminGroupAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Group
    template_name = 'account/dshb-group-add.html'
    form_class = GroupEditForm
    success_url = reverse_lazy('account_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminGroupEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Group
    template_name = 'account/dshb-group-edit.html'

    def get(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        group = get_object_or_404(Group, pk=group_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = GroupEditForm(instance=group)
        return render(request, 'account/dshb-group-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = GroupEditForm(request.POST, instance=get_object_or_404(Group, pk=kwargs.get('pk')))

        if form.is_valid():
            group = Group.objects.get(pk=kwargs.get('pk'))
            group.name = form.cleaned_data.get('name')
            group.course = form.cleaned_data.get('course')
            group.start_date = form.cleaned_data.get('start_date')
            group.end_date = form.cleaned_data.get('end_date')
            group.is_active = form.cleaned_data.get('is_active')
            group.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('account_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('account_dashboard')


# Course Student
class CourseStudentAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = CourseStudent
    template_name = 'account/dshb-course-student-add.html'
    form_class = CourseStudentEditForm
    success_url = reverse_lazy('account_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class CourseStudentEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = CourseStudent
    template_name = 'account/dshb-course-student-edit.html'

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        student = get_object_or_404(CourseStudent, pk=student_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = CourseStudentEditForm(instance=student)
        return render(request, 'account/dshb-course-student-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CourseStudentEditForm(request.POST, instance=get_object_or_404(CourseStudent, pk=kwargs.get('pk')))

        if form.is_valid():
            student = CourseStudent.objects.get(pk=kwargs.get('pk'))
            student.rating = form.cleaned_data.get('rating')
            student.is_active = form.cleaned_data.get('is_active')
            student.average = form.cleaned_data.get('average')
            student.payment = form.cleaned_data.get('payment')
            student.rest = form.cleaned_data.get('rest')
            student.group = form.cleaned_data.get('group')
            student.student = form.cleaned_data.get('student')
            student.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('account_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('account_dashboard')


class CourseStudentDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, *args, **kwargs):
        course_student_id = kwargs.get('pk')
        course_student = get_object_or_404(CourseStudent, pk=course_student_id)
        course_student.is_deleted = True
        course_student.save()
        messages.success(request, 'Təlim tələbəsi uğurla silindi')
        return redirect('account_dashboard')


# All Gallery
class AdminAllGalleryListView(AuthSuperUserCoordinatorMixin, ListView):
    model = AllGalery
    template_name = 'gallery/dshb-gallery.html'
    context_object_name = 'galleries'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        galleries = AllGalery.objects.all()
        context['videos'] = AllVideoGallery.objects.all()

        # Pagination
        page = self.request.GET.get('page')
        paginator = Paginator(galleries, self.paginate_by)

        try:
            galleries = paginator.page(page)
        except PageNotAnInteger:
            galleries = paginator.page(1)
        except EmptyPage:
            galleries = paginator.page(paginator.num_pages)

        context['galleries'] = galleries
        return context


class AdminAllGalleryDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = AllGalery.objects.get(pk=image_id)
            image.delete()
        except AllGalery.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Şəkil uğurla silindi')

        return redirect('gallery_dashboard')  # Redirect to the gallery dashboard page


class AdminAllGalleryAddView(AuthSuperUserCoordinatorMixin, FormView):
    model = AllGalery
    template_name = 'gallery/dshb-gallery_add.html'
    form_class = AllGaleryEditForm
    success_url = reverse_lazy('gallery_dashboard')

    def form_valid(self, form):
        uploaded_files = self.request.FILES.getlist('img')

        for uploaded_file in uploaded_files:
            AllGalery.objects.create(img=uploaded_file)

        messages.success(self.request, 'Şəkil uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Şəkil əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminAllGalleryDeleteAllView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request):
        # Delete all images in the AllGalery model
        AllGalery.objects.all().delete()
        messages.success(request, 'Bütün şəkillər uğurla silindi')
        return redirect('gallery_dashboard')


# All Video Gallery
class AdminAllVideoGalleryAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = AllVideoGallery
    template_name = 'gallery/dshb-gallery-video-add.html'
    form_class = AllVideoGalleryEditForm
    success_url = reverse_lazy('gallery_dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Video uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Video əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminAllVideoGalleryDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = AllVideoGallery.objects.get(pk=image_id)
            image.delete()
        except AllVideoGallery.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Video uğurla silindi')

        return redirect('gallery_dashboard')


# Subscriber
class AdminSubscriberView(AuthSuperUserCoordinatorMixin, ListView):
    model = Subscribe
    template_name = 'subscribe/dshb-subscribe-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s_query = self.request.GET.get('s', '')

        subscribers = Subscribe.objects.order_by('-created_at').all()

        if s_query:
            subscribers = subscribers.filter(
                Q(email__icontains=s_query) | Q(email__icontains=s_query)
            )

        context["subscribers"] = subscribers

        return context


class AdminSubscriberDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, email_id):
        try:
            email = Subscribe.objects.get(pk=email_id)
            email.delete()
        except Subscribe.DoesNotExist:
            pass
        messages.success(request, 'Şəkil uğurla silindi')

        return redirect('subscribe_dashboard')


# Course Gallery
class AdminAllCourseGalleryListView(AuthSuperUserCoordinatorMixin, ListView):
    model = Gallery
    template_name = 'course-gallery/dshb-course-gallery.html'
    context_object_name = 'galleries'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a_query = self.request.GET.get('a', '')
        v_query = self.request.GET.get('v', '')


        galleries = Gallery.objects.filter(course__status=True, course__is_delete=False, course__category__is_delete=False).all()
        videos = CourseVideo.objects.filter(course__status=True, course__is_delete=False).all()

        if a_query:
            galleries = galleries.filter(course__title__icontains=a_query)
        elif v_query:
            videos = videos.filter(course__title__icontains=v_query)
        context['videos'] = videos


        # Pagination
        page = self.request.GET.get('page')
        paginator = Paginator(galleries, self.paginate_by)

        try:
            galleries = paginator.page(page)
        except PageNotAnInteger:
            galleries = paginator.page(1)
        except EmptyPage:
            galleries = paginator.page(paginator.num_pages)

        context['galleries'] = galleries
        return context


class AdminAllCourseGalleryDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = Gallery.objects.get(pk=image_id)
            image.delete()
        except Gallery.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Şəkil uğurla silindi')

        return redirect('course_gallery_dashboard')


class AdminCourseGalleryAddView(AuthSuperUserCoordinatorMixin, FormView):
    model = Gallery
    template_name = 'course-gallery/dshb-course-gallery-add.html'
    form_class = GalLeryEditForm
    success_url = reverse_lazy('course_gallery_dashboard')

    def form_valid(self, form):
        # Get the selected course from the form
        selected_course = form.cleaned_data['course']

        uploaded_files = self.request.FILES.getlist('photo')

        for uploaded_file in uploaded_files:
            Gallery.objects.create(photo=uploaded_file, course=selected_course)

        messages.success(self.request, 'Şəkil uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Şəkil əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


# ********************************************************************************
# Course Video
class AdminCourseVideoAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = CourseVideo
    template_name = 'course-gallery/dshb-course-video-add.html'
    form_class = CourseVideoEditForm
    success_url = reverse_lazy('course_gallery_dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Video uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Video əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminCourseVideoDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = CourseVideo.objects.get(pk=image_id)
            image.delete()
        except CourseVideo.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Video uğurla silindi')

        return redirect('course_gallery_dashboard')


# TIM & TIM Image & TIM Video
class AdminTIMListView(AuthSuperUserCoordinatorMixin, ListView):
    model = TIM
    template_name = 'tim/dshb-tim.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['main_tim'] = TIM.objects.filter(status=True, is_delete=False).first()
        context['tim_images'] = TIMImage.objects.all()
        context['tim_videos'] = TIMVideo.objects.all()

        return context


class AdminTIMMainEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = TIM
    template_name = 'tim/dshb-tim-main-edit.html'

    def get(self, request, *args, **kwargs):
        about = TIM.objects.filter(status=True, is_delete=False).first()

        form = TIMEditForm(instance=about)
        return render(request, 'tim/dshb-tim-main-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TIMEditForm(request.POST, request.FILES, instance=TIM.objects.filter(status=True, is_delete=False).first())

        if form.is_valid():
            tim = TIM.objects.filter(status=True, is_delete=False).first()
            tim.title = form.cleaned_data.get('title')
            tim.description1 = form.cleaned_data.get('description1')
            # tim.description2 = form.cleaned_data.get('description2')
            tim.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('tim_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('tim_dashboard')


class AdminTIMImageAddView(AuthSuperUserCoordinatorMixin, FormView):
    model = TIMImage
    template_name = 'tim/tim-gallery/dshb-tim-image-add.html'
    form_class = TIMImageEditForm
    success_url = reverse_lazy('tim_dashboard')

    def form_valid(self, form):
        uploaded_files = self.request.FILES.getlist('photo')

        for uploaded_file in uploaded_files:
            TIMImage.objects.create(photo=uploaded_file)

        messages.success(self.request, 'Şəkil uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Şəkil əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminTIMImageDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = TIMImage.objects.get(pk=image_id)
            image.delete()
        except TIMImage.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Şəkil uğurla silindi')

        return redirect('tim_dashboard')


class AdminTIMVideoAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = TIMVideo
    template_name = 'tim/tim-gallery/dshb-tim-video-add.html'
    form_class = TIMVideoEditForm
    success_url = reverse_lazy('tim_dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Video uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Video əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminTIMVideoDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = TIMVideo.objects.get(pk=image_id)
            image.delete()
        except TIMVideo.DoesNotExist:
            # Handle the case where the image does not exist
            pass
        messages.success(request, 'Video uğurla silindi')

        return redirect('tim_dashboard')


# ***************************************************************************
# Certificate
class AdminCertificateListView(AuthSuperUserCoordinatorMixin, ListView):
    model = Certificate
    template_name = 'certificate/dshb-certificate.html'
    context_object_name = 'certificates'


class AdminCertificateDeleteView(AuthSuperUserCoordinatorMixin, DeleteView):
    def post(self, request, image_id):
        try:
            image = Certificate.objects.get(pk=image_id)
            image.delete()
        except Certificate.DoesNotExist:
            pass
        messages.success(request, 'Sertifikat uğurla silindi')

        return redirect('certificate_dashboard')


class AdminCertificateAddView(AuthSuperUserCoordinatorMixin, FormView):
    model = Certificate
    template_name = 'certificate/dshb-certificate-add.html'
    form_class = CertificateEditForm
    success_url = reverse_lazy('certificate_dashboard')

    def form_valid(self, form):
        uploaded_files = self.request.FILES.getlist('certificate')

        for uploaded_file in uploaded_files:
            Certificate.objects.create(certificate=uploaded_file)

        messages.success(self.request, 'Sertifikat uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Sertifikat əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


# COURSE TOPIC & COURSE TOPIC TEST
class AdminCourseTopicTestListView(AuthSuperUserCoordinatorTeacherMixin, ListView):
    model = CourseTopic
    template_name = 'course-topics-course-topic-test/dshb-course-topics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_query = self.request.GET.get('t', '')
        st_query = self.request.GET.get('st', '')
        tt_query = self.request.GET.get('tt', '')
        stt_query = self.request.GET.get('stt', '')

        topics = CourseTopic.objects.filter(is_deleted=False).order_by('-created_at').all()
        d_topics = CourseTopic.objects.filter(is_deleted=True).order_by('-created_at').all()
        topic_tests = CourseTopicsTest.objects.filter(is_deleted=False).order_by('-created_at').all()
        d_topic_tests = CourseTopicsTest.objects.filter(is_deleted=True).order_by('-created_at').all()

        if t_query:
            topics = topics.filter(
                Q(course__title__icontains=t_query) | Q(topic_title__icontains=t_query)
            )
        elif st_query:
            d_topics = d_topics.filter(
                Q(course__title__icontains=st_query) | Q(topic_title__icontains=st_query)
            )
        elif tt_query:
            topic_tests = topic_tests.filter(
                Q(name__icontains=tt_query) | Q(course__title__icontains=tt_query)
            )
        elif stt_query:
            d_topic_tests = d_topic_tests.filter(
                Q(name__icontains=stt_query) | Q(course__title__icontains=stt_query)
            )

        context["topics"] = topics
        context["d_topics"] = d_topics
        context["topic_tests"] = topic_tests
        context["d_topic_tests"] = d_topic_tests

        return context


class AdminCourseTopicDetailView(AuthSuperUserCoordinatorTeacherMixin, DetailView):
    model = CourseTopic
    template_name = 'course-topics-course-topic-test/dshb-course-topics-look.html'
    context_object_name = 'topic'


class AdminCourseTopicAddView(AuthSuperUserCoordinatorTeacherMixin, CreateView):
    model = CourseTopic
    template_name = 'course-topics-course-topic-test/dshb-course-topics-add.html'
    form_class = CourseTopicEditForm
    success_url = reverse_lazy('topic_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        context["tests"] = CourseTopicsTest.objects.all()
        return context

    def form_valid(self, form):
        course = self.request.POST.get('state')
        if course:
            course_instance = get_object_or_404(Course, pk=course)
            form.instance.course = course_instance
            form.instance.save()

        course_topics_test = self.request.POST.getlist('states[]')
        if course_topics_test:
            form.instance.course_topic_test.set(course_topics_test)


        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminCourseTopicEditView(AuthSuperUserCoordinatorTeacherMixin, CreateView):
    model = CourseTopic
    template_name = 'course-topics-course-topic-test/dshb-course-topics-edit.html'

    def get(self, request, *args, **kwargs):
        topic_pk = kwargs.get('pk')
        topic = get_object_or_404(CourseTopic, pk=topic_pk)

        form = CourseTopicEditForm(instance=topic)
        context = {
            'form': form,
            'courses': Course.objects.all(),
            'tests': CourseTopicsTest.objects.filter(course=topic.course).all(),
            'course_topic': topic,
        }
        return render(request, 'course-topics-course-topic-test/dshb-course-topics-edit.html', context)

    def post(self, request, *args, **kwargs):
        form = CourseTopicEditForm(request.POST, instance=get_object_or_404(CourseTopic, pk=kwargs.get('pk')))

        if form.is_valid():
            topic = CourseTopic.objects.get(pk=kwargs.get('pk'))
            topic.topic_title = form.cleaned_data.get('topic_title')

            course = self.request.POST.get('state')
            if course:
                course_instance = get_object_or_404(Course, pk=course)
                topic.course = course_instance

            course_topics_test = self.request.POST.getlist('states[]')
            if course_topics_test:
                topic.course_topic_test.set(course_topics_test)

            topic.save()

            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('topic_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('topic_dashboard')

# course-topic secilende ona uygun course topic testler cixmasi ucun api //
def get_course_topic_test_options(request):
    course_id = request.GET.get('course_id')
    course = get_object_or_404(Course, id=course_id)
    course_topic_tests = CourseTopicsTest.objects.filter(course=course)

    options = ''
    for topic_test in course_topic_tests:
        options += f'<option value="{topic_test.id}">{topic_test.name}</option>'

    return JsonResponse({'options': options})
# *******************************************

class AdminCourseTopicDeleteView(AuthSuperUserCoordinatorTeacherMixin, View):
    def post(self, request, *args, **kwargs):
        topic_id = kwargs.get('pk')
        topic = get_object_or_404(CourseTopic, pk=topic_id)
        topic.is_deleted = True
        topic.save()
        messages.success(request, 'Təlim mövzusu uğurla silindi')
        return redirect('topic_dashboard')


class AdminCourseTopicUndeleteView(AuthSuperUserCoordinatorTeacherMixin, View):
    def post(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(CourseTopic, pk=pk)
        topic.is_deleted = False
        topic.save()
        messages.success(request, 'Təlim mövzusu uğurla bərpa olundu')
        return redirect('topic_dashboard')


class AdminCourseTopicsTestAddView(AuthSuperUserCoordinatorTeacherMixin, CreateView):
    model = CourseTopicsTest
    template_name = 'course-topics-course-topic-test/dshb-course-topics-test-add.html'
    form_class = CourseTopicTestEditForm
    success_url = reverse_lazy('topic_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        return context

    def form_valid(self, form):
        course = self.request.POST.get('state')
        if course:
            course_instance = get_object_or_404(Course, pk=course)
            form.instance.course = course_instance
            form.instance.save()

        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminCourseTopicsTestEditView(AuthSuperUserCoordinatorTeacherMixin, CreateView):
    model = CourseTopicsTest
    template_name = 'course-topics-course-topic-test/dshb-course-topics-test-edit.html'

    def get(self, request, *args, **kwargs):
        test_pk = kwargs.get('pk')
        topic_test = get_object_or_404(CourseTopicsTest, pk=test_pk)

        form = CourseTopicTestEditForm(instance=topic_test)
        context = {
            'form': form,
            'courses': Course.objects.all(),
            'topic_test': topic_test,
        }
        return render(request, 'course-topics-course-topic-test/dshb-course-topics-test-edit.html', context)

    def post(self, request, *args, **kwargs):
        form = CourseTopicTestEditForm(request.POST, instance=get_object_or_404(CourseTopicsTest, pk=kwargs.get('pk')))

        if form.is_valid():
            topic_test = CourseTopicsTest.objects.get(pk=kwargs.get('pk'))
            topic_test.name = form.cleaned_data.get('name')

            course = self.request.POST.get('state')
            if course:
                course_instance = get_object_or_404(Course, pk=course)
                topic_test.course = course_instance

            topic_test.save()

            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('topic_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('topic_dashboard')


class AdminCourseTopicsTestDeleteView(AuthSuperUserCoordinatorTeacherMixin, View):
    def post(self, request, *args, **kwargs):
        topic_test_id = kwargs.get('pk')
        topic_test = get_object_or_404(CourseTopicsTest, pk=topic_test_id)
        topic_test.is_deleted = True
        topic_test.save()
        messages.success(request, 'Mövzu testi uğurla silindi')
        return redirect('topic_dashboard')


class AdminCourseTopicsTestUndeleteView(AuthSuperUserCoordinatorTeacherMixin, View):
    def post(self, request, pk, *args, **kwargs):
        topic_test = get_object_or_404(CourseTopicsTest, pk=pk)
        topic_test.is_deleted = False
        topic_test.save()
        messages.success(request, 'Mövzu testi uğurla bərpa olundu')
        return redirect('topic_dashboard')


# QUESTION & ANSWER
class AdminQuestionAnswerListView(AuthSuperUserCoordinatorTeacherMixin, ListView):
    model = CourseTopicsTest
    template_name = 'question/dshb-question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher_course = TeacherCourse.objects.filter(teacher=self.request.user)
        course_ids = teacher_course.values_list('course__id', flat=True)

        if self.request.user.staff_status == 'SuperUser':
            context['tests'] = CourseTopicsTest.objects.all()
        else:
            context['tests'] = CourseTopicsTest.objects.filter(course__id__in=course_ids)

        return context


# Question add page
class TopicTestDetailView(AuthSuperUserCoordinatorTeacherMixin, DetailView):
    model = CourseTopicsTest
    template_name = 'question/dshb-question-add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.filter(course_topic_test=self.object, is_active=True)
        context['questions'] = questions
        return context

    def post(self, request, *args, **kwargs):

        for key, value in request.POST.items():
            if key.startswith('title_'):
                q_id = key.split('_')[1]
                question = Question.objects.get(pk=q_id)
                question.question = value
                question.point = request.POST.get(f'point_{q_id}')
                question.save()

        for key, value in request.POST.items():
            if key.startswith('question_answer_'):
                q_id = key.split('_')[2]
                a_id = key.split('_')[3]
                answer = Answer.objects.get(question_id=q_id, id=a_id)
                answer.answer = value
                answer.is_correct = a_id == request.POST.get(f'answer_{q_id}')
                answer.save()

        for key, uploaded_file in request.FILES.items():
            if key.startswith('file_'):
                q_id = key.split('_')[1]
                question = Question.objects.get(pk=q_id)
                question.question_image = uploaded_file
                question.save()

        for key, value in request.POST.items():
            if key.startswith('delete_image_'):
                q_id = key.split('_')[2]
                question = Question.objects.get(pk=q_id)
                # Check if the checkbox is selected
                if value:
                    # Delete the image and clear the question_image field
                    question.question_image.delete()
                    question.question_image = None
                    question.save()

        # Create New Question
        for key, value in request.POST.items():
            if key.startswith('new_title_'):
                q_id = key.split('_')[2]
                question = Question.objects.create(
                    question=value,
                    point=request.POST.get(f'new_point_{q_id}'),
                    question_image = request.FILES.get(f'new_file_{q_id}'),
                    course_topic_test=self.get_object()
                )

                # Process new answers for the created question
                for sub_key, sub_value in request.POST.items():
                    if sub_key.startswith(f'new_question_answer_{q_id}_'):
                        a_id = sub_key.split('_')[-1]
                        answer = Answer.objects.create(
                            question=question,
                            answer=sub_value,
                            is_correct = a_id == request.POST.get(f'new_answer_{q_id}')
                        )

        # Delete Question
        for key, value in request.POST.items():
            if key.startswith('delete_question_'):
                q_id = key.split('_')[2]
                question = Question.objects.get(pk=q_id)
                question.is_active = False
                question.save()

        return redirect(reverse('topic_test_question', kwargs={'pk': self.get_object().pk}))


# STAFF ACCOUNT
class AdminStaffAccountListView(AuthSuperUserCoordinatorMixin, ListView):
    model = Account
    template_name = 'staff/dshb-staff-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        as_query = self.request.GET.get('as', '')
        das_query = self.request.GET.get('das', '')

        staff_users = Account.objects.exclude(staff_status='Tələbə').exclude(id=self.request.user.id).order_by('-id').all()

        if self.request.user.staff_status == 'SuperUser':
            staff_account = staff_users.filter(is_delete=False).all()
            d_staff_account = staff_users.filter(is_delete=True).all()
        elif self.request.user.staff_status == 'Koordinator':
            staff_account = staff_users.filter(is_delete=False).exclude(staff_status='SuperUser').all()
            d_staff_account = staff_users.filter(is_delete=True).exclude(staff_status='SuperUser').all()

        if as_query:
            staff_account = staff_account.filter(
                Q(first_name__icontains=as_query)
                | Q(last_name__icontains=as_query)
                | Q(id_code__icontains=as_query)
                | Q(FIN__icontains=as_query)
                | Q(email__icontains=as_query)
                | Q(number__icontains=as_query)
                | Q(staff_status__icontains=as_query)
                | Q(staff_course__course__title__icontains=as_query)
            )
        elif das_query:
            d_staff_account = d_staff_account.filter(
                Q(first_name__icontains=das_query)
                | Q(last_name__icontains=das_query)
                | Q(id_code__icontains=das_query)
                | Q(FIN__icontains=das_query)
                | Q(email__icontains=das_query)
                | Q(number__icontains=das_query)
                | Q(staff_status__icontains=das_query)
                | Q(staff_course__course__title__icontains=das_query)
            )

        context["staff_account"] = staff_account
        context["d_staff_account"] = d_staff_account

        return context


class AdminStaffAccountAddView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Account
    template_name = 'staff/dshb-staff-add.html'
    form_class = StaffAccountEditForm
    success_url = reverse_lazy('staff_dashboard')

    def get_form_kwargs(self):
        kwargs = super(AdminStaffAccountAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        fin = form.cleaned_data['FIN']
        form.instance.password = make_password(fin)
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminStaffAccountEditView(AuthSuperUserCoordinatorMixin, CreateView):
    model = Account
    template_name = 'staff/dshb-staff-edit.html'

    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('pk')
        account = get_object_or_404(Account, pk=account_id)

        # Create an instance of the CourseEditForm with the retrieved course
        form = StaffAccountEditForm(instance=account)
        return render(request, 'staff/dshb-staff-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StaffAccountEditForm(request.POST, instance=get_object_or_404(Account, pk=kwargs.get('pk')))

        if form.is_valid():
            account = Account.objects.get(pk=kwargs.get('pk'))
            account.first_name = form.cleaned_data.get('first_name')
            account.last_name = form.cleaned_data.get('last_name')
            # account.FIN = form.cleaned_data.get('FIN')
            account.staff_status = form.cleaned_data.get('staff_status')
            # account.id_code = form.cleaned_data.get('id_code')
            account.email = form.cleaned_data.get('email')
            account.number = form.cleaned_data.get('number')
            account.save()

            # Update the teacher's course if staff status is 'Müəllim' or 'Mentor'
            if account.staff_status in ['Müəllim', 'Mentor']:
                course = form.cleaned_data.get('course')
                if course:
                    teacher_course = TeacherCourse.objects.filter(teacher=account).first()

                    if teacher_course:
                        teacher_course.course = course
                        teacher_course.save()
                    else:
                        TeacherCourse.objects.create(teacher=account, course=course)

            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('staff_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('staff_dashboard')


class AdminStaffAccountDeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        account = get_object_or_404(Account, pk=pk)
        account.is_delete = True
        account.save()
        messages.success(request, 'İşçi uğurla silindi')
        return redirect('staff_dashboard')


class AdminStaffAccountUndeleteView(AuthSuperUserCoordinatorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        account = get_object_or_404(Account, pk=pk)
        account.is_delete = False
        account.save()
        messages.success(request, 'İşçi uğurla bərpa olundu')
        return redirect('staff_dashboard')
