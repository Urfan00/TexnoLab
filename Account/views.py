from django.shortcuts import redirect, render
from Account.models import Account
from Course.models import CourseStudent
from services.uploader import Uploader
from .forms import AccountInforrmationForm, ChangePasswordForm, CustomSetPasswordForm, LoginForm, ResetPasswordForm, SocialProfileForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View



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
        context["my_course"] = CourseStudent.objects.filter(student=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        form1 = AccountInforrmationForm(instance=request.user)
        form2 = SocialProfileForm(instance=request.user)
        return render(request, self.template_name, {**self.get_context_data(), 'form1': form1, 'form2': form2})

    def post(self, request, *args, **kwargs):
        form1 = AccountInforrmationForm(request.POST, request.FILES)
        form2 = SocialProfileForm(request.POST)

        if form1.is_valid():
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
        elif form2.is_valid():
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
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('profile')
