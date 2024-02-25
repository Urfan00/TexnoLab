from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm,
                                      UsernameField,
                                      PasswordResetForm,
                                      PasswordChangeForm,
                                      SetPasswordForm)

# from Account.models import Certificate


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

    error_messages = {
        'invalid_login': "Daxil etdiyiniz İD kod və ya şifrə yanlışdır. Zəhmət olmasa, doğru daxil edin.",
        'inactive': "Hesabınız aktiv deyil.",
    }


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

    error_messages = {
        'password_incorrect': 'Cari şifrə yanlışdır. Zəhmət olmasa, düzgün daxil edin.',
        'password_mismatch': 'Yeni şifrələr uyğun gəlmir. Zəhmət olmasa, təkrar daxil edin.',
        # 'password_invalid': 'Yeni şifrə etibarsızdır. Zəhmət olmasa, başqa bir şifrə seçin.',
        # 'password_same_as_username': 'Şifrə istifadəçi adı ilə eyni ola bilməz. Zəhmət olmasa, başqa bir şifrə seçin.',
        # 'password_too_common': 'Şifrə çox yayğın və rahatlıqla təxmin edilə bilən bir şifrədir. Zəhmət olmasa, daha güclü bir şifrə seçin.',
        # 'password_entirely_numeric': 'Şifrə tamamilə rəqəmlərdən ibarət ola bilməz. Zəhmət olmasa, daha çeşidlənmiş bir şifrə seçin.',
        # 'password_too_short': 'Şifrə çox qısa. Zəhmət olmasa, minimum 8 simvol daxil edin.',
        # 'password_common_sequences': 'Şifrədə yayğın ardıcıllıqlardan istifadə etmək təhlükəlidir. Zəhmət olmasa, daha güclü bir şifrə seçin.',
    }



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
        fields = ['bio', 'email', "number", 'feedback', 'cv']
        labels = {
            'number' : 'Əlaqə nömrəsi',
            'email' : 'E-poçt',
            # 'image' : 'Profil şəkli',
            'feedback' : 'Texnolab haqqında rəyiniz',
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
