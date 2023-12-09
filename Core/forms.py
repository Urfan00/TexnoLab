from django import forms
from .models import Certificate, ContactUs, Subscribe
from multiupload.fields import MultiFileField


class ContactFormModel(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['fullname', 'email', 'message']
        labels = {
            'fullname' : 'Ad, soyad',
            'email' : 'E-poçt',
            'message' : 'Mesaj'
        }
        widgets = {
            'fullname' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"",
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :""
                }
            ),
            'message' : forms.Textarea(
                attrs={
                    'class' : 'form-control',
                    'rows' : 7,
                    'placeholder' :""
                }
            ),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']
        labels = {
            'email' : 'E-poçt',
        }
        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"E-poçt daxil edin ..."
                }
            )
        }


class CertificateEditForm(forms.ModelForm):
    certificate = MultiFileField(min_num=1, max_num=50, max_file_size=1024*1024*5)

    class Meta:
        model = Certificate
        fields = ['certificate']
