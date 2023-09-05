from django.shortcuts import redirect
from .forms import ChangePasswordForm, CustomSetPasswordForm, LoginForm, ResetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy



class LogInView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name='change-password.html'
    form_class= ChangePasswordForm
    success_url = reverse_lazy('logout')


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
    success_url = reverse_lazy('reset_password_complete')
