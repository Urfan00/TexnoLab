from django import forms
from .models import ContactUs


class ContactFormModel(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['fullname', 'email', 'message']
        labels = {
            'fullname' : 'Ad, soyad',
            'email' : 'E-poçts',
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

