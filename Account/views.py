from .forms import ChangePasswordForm, CustomSetPasswordForm, LoginForm, ResetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy


class LogInView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name='change_password.html'
    form_class= ChangePasswordForm
    success_url = reverse_lazy('login')


class ResetPasswordView(PasswordResetView):
    template_name = 'forget_pwd.html'
    form_class = ResetPasswordForm
    email_template_name = 'reset_password_email.html'
    subject_template_name = 'reset_password_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      "If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."

    success_url = reverse_lazy('login')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name='reset_password_confirm.html'
    form_class=CustomSetPasswordForm
    success_url = reverse_lazy('reset_password_complete')
