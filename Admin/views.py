from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from Account.models import Account
from Core.models import Partner
from .forms import BlogCategoryEditForm, BlogEditForm, CourseCategoryEditForm, CourseEditForm, CourseProgramEditForm, PartnerEditForm, RequestUsAdminCommentForm, ServiceEditForm
from Blog.models import Blog, BlogCategory
from Course.models import Course, CourseCategory, CourseFeedback, CourseProgram, CourseStatistic, RequestUs
from Service.models import Service
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

# **********************************************************************************
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        # Customize the behavior when the user is not staff
        raise PermissionDenied("You do not have permission to access this page.")
# **********************************************************************************


class DashboardView(StaffRequiredMixin, ListView):
    model = Account
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_count'] = Account.objects.count()
        context['blog_count'] = Blog.objects.count()
        context['course_count'] = Course.objects.count()
        context['service_count'] = Service.objects.count()
        context["courses"] = Course.objects.annotate(review_count=Count('course_feedback'), program_count=Count('course_program'), student_count=Count('student_course')).order_by('-created_at').all()[:5]
        context["blogs"] = Blog.objects.filter(is_delete=False).order_by('-created_at').all()[:5]
        context["services"] = Service.objects.order_by('-created_at').all()[:5]
        return context

# *************************************************************************************

# COURSE & COURSE CATEGORY
class AdminCourseListView(StaffRequiredMixin, ListView):
    model = Course
    template_name = 'course/dshb-courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a_query = self.request.GET.get('a', '')
        d_query = self.request.GET.get('d', '')
        sc_query = self.request.GET.get('sc', '')
        k_query = self.request.GET.get('k', '')
        sk_query = self.request.GET.get('sk', '')

        # Filter active courses
        active_courses = Course.objects.filter(status=True, is_delete=False).order_by('-start_date')
        
        # Filter inactive courses
        deactive_courses = Course.objects.filter(status=False, is_delete=False).order_by('-start_date')

        delete_courses = Course.objects.filter(is_delete=True).order_by('-start_date')

        categories = CourseCategory.objects.filter(is_delete=False).order_by('-created_at')

        deleted_categories = CourseCategory.objects.filter(is_delete=True).order_by('-created_at')


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


        context["active_course"] = active_courses
        context["deactive_course"] = deactive_courses
        context["delete_course"] = delete_courses
        context["categories"] = categories
        context["deleted_categories"] = deleted_categories


        return context


# COURSE
class AdminCourseEditView(StaffRequiredMixin, CreateView):
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
            course.start_date = form.cleaned_data.get('start_date')
            course.status = form.cleaned_data.get('status')
            course.end_date = form.cleaned_data.get('end_date')
            course.category = form.cleaned_data.get('category')
            course.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('course_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('course_dashboard')


class AdminCourseAddView(StaffRequiredMixin, CreateView):
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


class AdminCourseDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        course.is_delete = True
        course.save()
        messages.success(request, 'Course deleted successfully')
        return redirect('course_dashboard')


class AdminCourseUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        course.is_delete = False  # Set is_delete to False to undelete
        course.save()
        messages.success(request, 'Course undeleted successfully')
        return redirect('course_dashboard')


# COURSE CATEGORY
class AdminCourseCategoryEditView(StaffRequiredMixin, CreateView):
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


class AdminCourseCategoryAddView(StaffRequiredMixin, CreateView):
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


class AdminCourseCategoryDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(CourseCategory, pk=pk)
        course.is_delete = True
        course.save()
        messages.success(request, 'Course Category deleted successfully')
        return redirect('course_dashboard')


class AdminCourseCategoryUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(CourseCategory, pk=pk)
        course.is_delete = False  # Set is_delete to False to undelete
        course.save()
        messages.success(request, 'Course Category undeleted successfully')
        return redirect('course_dashboard')


# ********************************************************************************

# BLOG & BLOG CATEGORY
class AdminBlogListView(StaffRequiredMixin, ListView):
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
class AdminBlogAddView(StaffRequiredMixin, CreateView):
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


class AdminBlogEditView(StaffRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/dshb-listing-blog.html'

    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get('slug')  # Get the course ID from URL kwargs
        blog = get_object_or_404(Blog, slug=blog_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = BlogEditForm(instance=blog)
        return render(request, 'blog/dshb-listing-blog-category.html', {'form': form})

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


class AdminBlogDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        blog_id = kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        blog.is_delete = True
        blog.save()
        messages.success(request, 'Blog deleted successfully')
        return redirect('blog_dashboard')


class AdminBlogUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        blog.is_delete = False  # Set is_delete to False to undelete
        blog.save()
        messages.success(request, 'Blog undeleted successfully')
        return redirect('blog_dashboard')


# BLOG CATEGORY
class AdminBlogCategoryAddView(StaffRequiredMixin, CreateView):
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


class AdminBlogCategoryEditView(StaffRequiredMixin, CreateView):
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


class AdminBlogCategoryDeleteView(StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = get_object_or_404(BlogCategory, pk=category_id)
        category.is_delete = True
        category.save()
        messages.success(request, 'Blog Category deleted successfully')
        return redirect('blog_dashboard')


class AdminBlogCategoryUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(BlogCategory, pk=pk)
        category.is_delete = False  # Set is_delete to False to undelete
        category.save()
        messages.success(request, 'Blog Category undeleted successfully')
        return redirect('blog_dashboard')

# ********************************************************************************


# Service
class AdminServiceListView(StaffRequiredMixin, ListView):
    model = Service
    template_name = 'service/dshb-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a_query = self.request.GET.get('a', '')
        d_query = self.request.GET.get('d', '')
        ss_query = self.request.GET.get('ss', '')
        # c_query = self.request.GET.get('c', '')
        # sc_query = self.request.GET.get('sc', '')

        active_service = Service.objects.filter(status=True, is_delete=False).order_by('-created_at')
        deactive_service = Service.objects.filter(status=False, is_delete=False).order_by('-created_at')
        delete_service = Service.objects.filter(is_delete=True).order_by('-created_at')

        # category = BlogCategory.objects.filter(is_delete=False).order_by('-created_at').all()
        # delete_category = BlogCategory.objects.filter(is_delete=True).order_by('-created_at').all()

        # Apply search filter if a query is provided
        if a_query:
            active_service = active_service.filter(title__icontains=a_query)
        elif d_query:
            deactive_service = deactive_service.filter(title__icontains=d_query)
        elif ss_query:
            delete_service = delete_service.filter(title__icontains=ss_query)
        # elif c_query:
        #     category = category.filter(name__icontains=c_query)
        # elif sc_query:
        #     delete_category = category.filter(name__icontains=sc_query)


        context["active_services"] = active_service
        context["deactive_services"] = deactive_service
        context["delete_services"] = delete_service
        # context["categories"] = category
        # context["delete_category"] = delete_category

        return context


class AdminServiceAddView(StaffRequiredMixin, CreateView):
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


class AdminServiceEditView(StaffRequiredMixin, CreateView):
    model = Service
    template_name = 'service/dshb-listing-service.html'

    def get(self, request, *args, **kwargs):
        service_id = kwargs.get('slug')  # Get the course ID from URL kwargs
        service = get_object_or_404(Service, slug=service_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = ServiceEditForm(instance=service)
        return render(request, 'service/dshb-listing-service.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ServiceEditForm(request.POST, instance=get_object_or_404(Service, slug=kwargs.get('slug')))

        if form.is_valid():
            service = Service.objects.get(slug=kwargs.get('slug'))
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


class AdminServiceDeleteView(StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        service = get_object_or_404(Service, pk=service_id)
        service.is_delete = True
        service.save()
        messages.success(request, 'Service deleted successfully')
        return redirect('service_dashboard')


class AdminServiceUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        service = get_object_or_404(Service, pk=pk)
        service.is_delete = False  # Set is_delete to False to undelete
        service.save()
        messages.success(request, 'Service undeleted successfully')
        return redirect('service_dashboard')


# ********************************************************************************
# Course Statistic & Request US & Feedback & Program
class AdminCourseSRFPListView(StaffRequiredMixin, ListView):
    model = CourseStatistic
    template_name = 'course/feedback-request-statistic-c_program/dshb-courses-frsp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ks_query = self.request.GET.get('ks', '')
        f_query = self.request.GET.get('f', '')
        df_query = self.request.GET.get('df', '')
        m_query = self.request.GET.get('m', '')
        bm_query = self.request.GET.get('bm', '')
        dr_query = self.request.GET.get('dr', '')
        p_query = self.request.GET.get('p', '')
        sp_query = self.request.GET.get('sp', '')

        statistics = CourseStatistic.objects.all()

        feedbacks = CourseFeedback.objects.filter(is_delete=False).all()
        d_feedbacks = CourseFeedback.objects.filter(is_delete=True).all()

        request_us = RequestUs.objects.filter(is_view=False, is_delete=False).all()
        b_request_us = RequestUs.objects.filter(is_view=True, is_delete=False).all()
        d_request_us = RequestUs.objects.filter(is_delete=True).all()

        programs = CourseProgram.objects.filter(is_delete=False).all()
        d_programs = CourseProgram.objects.filter(is_delete=True).all()

        # active_service = Service.objects.filter(status=True, is_delete=False).order_by('-created_at')

        if ks_query:
            statistics = statistics.filter(course__title__icontains=ks_query)
        elif f_query:
            feedbacks = feedbacks.filter(
                Q(course__title__icontains=f_query) | Q(student__first_name__icontains=f_query) | Q(student__last_name__icontains=f_query)
            )
        elif df_query:
            d_feedbacks = d_feedbacks.filter(
                Q(course__title__icontains=df_query) | Q(student__first_name__icontains=df_query) | Q(student__last_name__icontains=df_query)
            )
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
        elif p_query:
            programs = programs.filter(
                Q(course__title__icontains=p_query) | Q(program_name__icontains=p_query)
            )
        elif sp_query:
            d_programs = d_programs.filter(
                Q(course__title__icontains=sp_query) | Q(program_name__icontains=sp_query)
            )


        context["statistics"] = statistics
        context["feedbacks"] = feedbacks
        context["d_feedbacks"] = d_feedbacks
        context["request_us"] = request_us
        context["b_request_us"] = b_request_us
        context["d_request_us"] = d_request_us
        context["programs"] = programs
        context["d_programs"] = d_programs

        return context


# Feedback
class AdminCourseSRFPFeedbackDeleteView(StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        feedback_id = kwargs.get('pk')
        feedback = get_object_or_404(CourseFeedback, pk=feedback_id)
        feedback.is_delete = True
        feedback.save()
        messages.success(request, 'Feedback deleted successfully')
        return redirect('course_srfp')


class AdminCourseSRFPFeedbackUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        feedback = get_object_or_404(CourseFeedback, pk=pk)
        feedback.is_delete = False  # Set is_delete to False to undelete
        feedback.save()
        messages.success(request, 'Feedback undeleted successfully')
        return redirect('course_srfp')


class AdminCourseSRFPDetailView(StaffRequiredMixin, DetailView):
    model = CourseFeedback
    template_name = 'course/feedback-request-statistic-c_program/dshb-courses-frsp-look.html'
    context_object_name = 'feedback'


# Request US
class AdminCourseSRFPRequestUsDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(RequestUs, pk=pk)
        course.is_delete = True
        course.save()
        messages.success(request, 'Request Us deleted successfully')
        return redirect('course_srfp')


class AdminCourseSRFPRequestUsUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(RequestUs, pk=pk)
        course.is_delete = False  # Set is_delete to False to undelete
        course.save()
        messages.success(request, 'Request Us undeleted successfully')
        return redirect('course_srfp')


class AdminCourseSRFPRequestUsDetailView(StaffRequiredMixin, DetailView, CreateView):
    model = RequestUs
    template_name = 'course/feedback-request-statistic-c_program/dshb-courses-frsp-look-request.html'
    context_object_name = 'request'
    form_class = RequestUsAdminCommentForm

    # def get(self, request, *args, **kwargs):
    #     request_us = RequestUs.objects.get(pk=self.get_object().pk)
    #     request_us.is_view = True
    #     request_us.save()
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        if form.is_valid():
            # Your code to save the admin_comment here
            request_us = RequestUs.objects.get(pk=self.get_object().pk)
            request_us.admin_comment = form.cleaned_data['admin_comment']
            request_us.is_view = True
            request_us.save()
            messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
            return redirect("request_us_look", pk=self.kwargs.get('pk'))
        else:
            messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
            return redirect("request_us_look", pk=self.kwargs.get('pk'))


# Program
class AdminCourseProgramAddView(StaffRequiredMixin, CreateView):
    model = CourseProgram
    template_name = 'course/feedback-request-statistic-c_program/dshb-listing-course-program-add.html'
    form_class = CourseProgramEditForm
    success_url = reverse_lazy('course_srfp')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminCourseProgramEditView(StaffRequiredMixin, CreateView):
    model = CourseProgram
    template_name = 'course/feedback-request-statistic-c_program/dshb-listing-course-program-edit.html'

    def get(self, request, *args, **kwargs):
        program_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        program = get_object_or_404(CourseProgram, pk=program_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = CourseProgramEditForm(instance=program)
        return render(request, 'course/feedback-request-statistic-c_program/dshb-listing-course-program-edit.html', {'form': form})

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
            return redirect('course_srfp')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('course_srfp')


class AdminCourseProgramDeleteView(StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        program_id = kwargs.get('pk')
        program = get_object_or_404(CourseProgram, pk=program_id)
        program.is_delete = True
        program.save()
        messages.success(request, 'Course Program deleted successfully')
        return redirect('course_srfp')


class AdminCourseProgramUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        program = get_object_or_404(CourseProgram, pk=pk)
        program.is_delete = False  # Set is_delete to False to undelete
        program.save()
        messages.success(request, 'Course Program undeleted successfully')
        return redirect('course_srfp')


# ********************************************************************************
# Partner & Contact US & FAQ
class AdminContactUSFAQPartnersListView(StaffRequiredMixin, ListView):
    model = CourseStatistic
    template_name = 'core/partner-faq-contact_us/dshb-courses-p-faq-c_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_query = self.request.GET.get('p', '')
        sp_query = self.request.GET.get('sp', '')
        # ks_query = self.request.GET.get('ks', '')
        # f_query = self.request.GET.get('f', '')
        # df_query = self.request.GET.get('df', '')
        # m_query = self.request.GET.get('m', '')
        # bm_query = self.request.GET.get('bm', '')
        # dr_query = self.request.GET.get('dr', '')

        partners = Partner.objects.filter(is_delete=False).order_by('-created_at').all()
        d_partners = Partner.objects.filter(is_delete=True).order_by('-created_at').all()


        # statistics = CourseStatistic.objects.all()
        # feedbacks = CourseFeedback.objects.filter(is_delete=False).all()
        # d_feedbacks = CourseFeedback.objects.filter(is_delete=True).all()
        # request_us = RequestUs.objects.filter(is_view=False, is_delete=False).all()
        # b_request_us = RequestUs.objects.filter(is_view=True, is_delete=False).all()
        # d_request_us = RequestUs.objects.filter(is_delete=True).all()


        # # active_service = Service.objects.filter(status=True, is_delete=False).order_by('-created_at')

        if p_query:
            partners = partners.filter(title__icontains=p_query)
        elif sp_query:
            d_partners = d_partners.filter(title__icontains=sp_query)


        context["partners"] = partners
        context["d_partners"] = d_partners

        return context


# Partner
class AdminPartnerAddView(StaffRequiredMixin, CreateView):
    model = Partner
    template_name = 'core/partner-faq-contact_us/partners/dshb-partner-add.html'
    form_class = PartnerEditForm
    success_url = reverse_lazy('core_dashboard')

    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'Məlumatlarınız uğurla əlavə edildi')
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form has validation errors, display an error message
        messages.error(self.request, 'Məlumatlarınız əlavə edilmədi. Zəhmət olmasa düzgün doldurun.')
        return super().form_invalid(form)


class AdminPartnerEditView(StaffRequiredMixin, CreateView):
    model = Partner
    template_name = 'core/partner-faq-contact_us/partners/dshb-partner-edit.html'

    def get(self, request, *args, **kwargs):
        partner_id = kwargs.get('pk')  # Get the course ID from URL kwargs
        partner = get_object_or_404(Partner, pk=partner_id)  # Retrieve the Course instance

        # Create an instance of the CourseEditForm with the retrieved course
        form = PartnerEditForm(instance=partner)
        return render(request, 'core/partner-faq-contact_us/partners/dshb-partner-edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PartnerEditForm(request.POST, request.FILES, instance=get_object_or_404(Partner, pk=kwargs.get('pk')))

        if form.is_valid():
            partner = Partner.objects.get(pk=kwargs.get('pk'))
            partner.title = form.cleaned_data.get('title')
            partner.img = form.cleaned_data.get('img')
            partner.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('core_dashboard')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('core_dashboard')


class AdminPartnerDeleteView(StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        partner_id = kwargs.get('pk')
        partner = get_object_or_404(Partner, pk=partner_id)
        partner.is_delete = True
        partner.save()
        messages.success(request, 'Partner deleted successfully')
        return redirect('core_dashboard')


class AdminPartnerUndeleteView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        partner = get_object_or_404(Partner, pk=pk)
        partner.is_delete = False  # Set is_delete to False to undelete
        partner.save()
        messages.success(request, 'Partner undeleted successfully')
        return redirect('core_dashboard')




