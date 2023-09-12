from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                      AuthenticationForm,
                                      UsernameField,
                                      PasswordResetForm,
                                      PasswordChangeForm,
                                      SetPasswordForm)


User = get_user_model()

# LOGIN FORM
class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder' : 'ID Kod'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder' : 'Şifrə'
            }
        )
    )


# CHANGE PASSWORD FORM
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label='Cari şifrə',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Cari şifrə'
            }))
    new_password1 = forms.CharField(required=True, label='Yeni şifrə',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Yeni şifrə'
            }))
    new_password2 = forms.CharField(required=True, label='Yeni şifrənin təsdiqi',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Yeni şifrənin təsdiqi'
            }))


# Forgot password EMAIL
class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder' : 'E-poçtunuzu daxil edin'
            }
        )
    )


# PASSWORD RESET
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True, label='New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '********'
            }))
    new_password2 = forms.CharField(required=True, label='Confirm New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '********'
            }))

