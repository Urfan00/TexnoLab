from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm,
                                      UsernameField,
                                      PasswordResetForm,
                                      PasswordChangeForm,
                                      SetPasswordForm)

from Account.models import Certificate


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


class AccountInforrmationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'email', "number", 'feedback', 'image', 'cv']
        labels = {
            'number' : 'Əlaqə nömrəsi',
            'email' : 'E-poçt',
            'image' : 'Profil şəkli',
            'feedback' : 'Kurs haqıında rəyiniz',
            'bio' : 'Haqqınızda məlumat',
            'cv' : 'CV',
        }
        widgets = {
            'number' : forms.TextInput(
                attrs={
                    # 'class' : 'form-control',
                    'placeholder' : "Enter your number",
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    # 'class' : 'form-control',
                    'placeholder' :"E-mail address"
                }
            ),
            'feedback' : forms.Textarea(
                attrs={
                    # 'class' : 'form-control',
                    'rows' : 7,
                    'placeholder' :""
                }
            ),
            'bio' : forms.Textarea(
                attrs={
                    # 'class' : 'form-control',
                    'rows' : 7,
                    'placeholder' :""
                }
            ),
        }


class SocialProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn']
        labels = {
            'instagram' : 'İnstagram',
            'twitter' : 'Twitter',
            'facebook' : 'Facebook',
            'github' : 'Github',
            'youtube' : 'YouTube',
            'linkedIn' : 'LinkedIn'
        }
        widgets = {
            'instagram' : forms.URLInput(
                attrs={
                    'class': 's',
                    'placeholder' :"",
                    
                }
            ),
            'twitter' : forms.URLInput(
                attrs={
                    'class': 's',
                    'placeholder' :""
                }
            ),
            'facebook' : forms.URLInput(
                attrs={
                    'class': 's',
                    'placeholder' :""
                }
            ),
            'github' : forms.URLInput(
                attrs={
                    'class': 's',
                    'placeholder' :""
                }
            ),
            'youtube' : forms.URLInput(
                attrs={
                    'class': 's',
                    'placeholder' :""
                }
            ),
            'linkedIn' : forms.URLInput(
                attrs={
                    'class': 's',
                    'placeholder' :""
                }
            ),
        }


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate', 'student']
        widgets = {
            'student' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            )
        }
