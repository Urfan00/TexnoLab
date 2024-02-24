from django.shortcuts import redirect, render
from Account.models import Account
from ExamResult.models import CourseStudent, Group, StudentResult
from services.mixins import AuthSuperUserTeacherMixin
from .forms import AccountInforrmationForm, ChangePasswordForm, CustomSetPasswordForm, LoginForm, ResetPasswordForm, SocialProfileForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.db.models import Subquery, Avg, Case, When, F, Value, CharField



def logout_view(request):
    logout(request)
    return redirect('login')


class LogInView(LoginView, UserPassesTestMixin):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'first_time_login') and self.request.user.first_time_login:
                # If user is authenticated and has first_time_login attribute set
                return reverse_lazy('change_password')
            elif next_url:
                # If there's a next_url parameter in the URL, redirect to that
                return next_url
            else:
                if self.request.user.staff_status == 'Tələbə':
                    return reverse_lazy('student_dashboard')
                elif self.request.user.staff_status == 'SuperUser' or self.request.user.staff_status == 'Koordinator':
                    return reverse_lazy('dashboard')
                elif self.request.user.staff_status == 'Müəllim':
                    return reverse_lazy('evaluation')
                elif self.request.user.staff_status == 'Mentor':
                    return reverse_lazy('lab_evaluation')
                else:
                    return reverse_lazy('index')
        return reverse_lazy('index')  # For anonymous users


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name='change-password.html'
    form_class= ChangePasswordForm
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        # Call the parent class's form_valid method to perform the password change

        # Update the first_time_login attribute to False
        self.request.user.first_time_login = False
        self.request.user.save()

        return super().form_valid(form)


class ResetPasswordView(PasswordResetView):
    template_name = 'reset_pwd/forget-password.html'
    form_class = ResetPasswordForm
    email_template_name = 'reset_pwd/reset_password_email.html'
    subject_template_name = 'reset_pwd/reset_password_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      "If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."

    success_url = reverse_lazy('logout')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name='reset_pwd/reset_password_confirm.html'
    form_class=CustomSetPasswordForm
    success_url = reverse_lazy('logout')


class AccountInformationView(LoginRequiredMixin, View):
    model = Account
    template_name = 'dshb-settings.html'

    def get_context_data(self):
        context = {}

        position = self.request.user.staff_status
        context['position'] = position

        if position == 'Tələbə':
            context["my_course"] = CourseStudent.objects.filter(student=self.request.user)

        return context

    def get(self, request, *args, **kwargs):
        form1 = AccountInforrmationForm(instance=request.user)
        form2 = SocialProfileForm(instance=request.user)
        change_password_form = ChangePasswordForm(user=request.user)  # Instantiate the form

        return render(request, self.template_name, {
            **self.get_context_data(),
            'form1': form1,
            'form2': form2,
            'change_password_form': change_password_form,  # Add the form to the context
        })

    def post(self, request, *args, **kwargs):
        form1 = AccountInforrmationForm(request.POST, request.FILES)
        form2 = SocialProfileForm(request.POST)
        change_password_form = ChangePasswordForm(user=request.user, data=request.POST)  # Instantiate the form with POST data

        if form1.is_valid() and self.request.POST.get('form_name') == 'form1':
            user_account = Account.objects.get(pk=request.user.pk)
            user_account.number = form1.cleaned_data.get('number')
            user_account.email = form1.cleaned_data.get('email')
            user_account.feedback = form1.cleaned_data.get('feedback')
            user_account.bio = form1.cleaned_data.get('bio')
            if form1.cleaned_data.get('image'):
                user_account.image = form1.cleaned_data.get('image')
            if form1.cleaned_data.get('cv'):
                user_account.cv = form1.cleaned_data.get('cv')
            user_account.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('profile')

        elif form2.is_valid() and self.request.POST.get('form_name') == 'form2':
            user_account = Account.objects.get(pk=request.user.pk)
            user_account.instagram = form2.cleaned_data.get('instagram')
            user_account.twitter = form2.cleaned_data.get('twitter')
            user_account.facebook = form2.cleaned_data.get('facebook')
            user_account.github = form2.cleaned_data.get('github')
            user_account.youtube = form2.cleaned_data.get('youtube')
            user_account.linkedIn = form2.cleaned_data.get('linkedIn')
            user_account.save()
            messages.success(request, 'Məlumatlarınız uğurla yeniləndi')
            return redirect('profile')

        elif self.request.POST.get('form_name') == 'change_password_form':
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)  # Important!
                self.request.user.first_time_login = False
                self.request.user.save()

                messages.success(request, 'Şifrə uğurla dəyişdirildi.')
                return redirect('profile')
            else:
                # Retrieve form errors
                change_password_errors = change_password_form.errors
                return render(request, self.template_name, {
                    **self.get_context_data(),
                    'form1': form1,
                    'form2': form2,
                    'change_password_form': change_password_form,
                    'change_password_errors': change_password_errors,  # Pass errors to the template
                })
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('profile')


class ResultView(AuthSuperUserTeacherMixin, ListView):
    model = StudentResult
    template_name = 'dshb-results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        g_query = self.request.GET.get('state', '')
        t_query = self.request.GET.get('t', '')

        user_account = Account.objects.filter(id=self.request.user.id, staff_status='Müəllim').first()
        super_user = Account.objects.filter(id=self.request.user.id, staff_status='SuperUser').first()

        if user_account or super_user:
            if user_account:
                teacher_courses = user_account.staff_course.values_list('course', flat=True)
                groups = Group.objects.filter(course__id__in=teacher_courses, is_active=True).all()
            elif super_user:
                groups = Group.objects.filter(is_active=True).all()

            context['groups'] = groups

            if g_query:
                group_topics = Group.objects.filter(id=g_query, is_active=True).first()
                context['group_topics'] = group_topics
                if t_query:
                    # course_students = CourseStudent.objects.filter(group=g_query, group_student_is_active=True).all()
                    # secilen qrup ve topice gore netice
                    context['students_results'] = StudentResult.objects.filter(
                        # student__in=Subquery(course_students.values('student')),
                        s_r_group = g_query,
                        exam_topics = t_query,
                    ).order_by('-total_point')

                    all_topics = group_topics.all_course_topics.all()

                    # Retrieve student results for the given group
                    students_all_results = StudentResult.objects.filter(
                        s_r_group=g_query
                    ).values('student__id', 'student__first_name', 'student__last_name').annotate(
                        # avg_total_point=Avg('total_point') * 5 # faizle ortalamsi
                        avg_total_point=Avg('total_point')
                    ).order_by('-avg_total_point')

                    # Iterate over each student result to calculate other_topics_total_points
                    for student_result in students_all_results:
                        student_id = student_result['student__id']
                        student_result['other_topics_total_points'] = []
                        for topic in all_topics:
                            topic_result = StudentResult.objects.filter(student_id=student_id, exam_topics=topic).first()
                            if topic_result:
                                # student_result['other_topics_total_points'].append(topic_result.total_point * 5) # fazile neticesi
                                student_result['other_topics_total_points'].append(topic_result.total_point)
                            else:
                                student_result['other_topics_total_points'].append('-------')

                    context['all_results'] = students_all_results


        return context
