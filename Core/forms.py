from django import forms
from .models import ContactUs


class ContactFormModel(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['fullname', 'email', 'message']
        labels = {
            'fullname' : 'Fullname',
            'email' : 'Email',
            'message' : 'Message'
        }
        widgets = {
            'fullname' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"Fullname",
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"E-mail address"
                }
            ),
            'message' : forms.Textarea(
                attrs={
                    'class' : 'form-control',
                    'rows' : 7,
                    'placeholder' :"Write your message"
                }
            ),
        }

