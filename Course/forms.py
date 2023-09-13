from django import forms
from .models import CourseFeedback, RequestUs


class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['message']
        labels = {
            'message' : 'Message'
        }
        widgets = {
            'message' : forms.Textarea(
                attrs={
                    'class' : 'form-control',
                    'rows' : 8,
                    'placeholder' :"Write your message"
                }
            )
        }


class RequestUsForm(forms.ModelForm):
    class Meta:
        model = RequestUs
        fields = ['fullname', 'phone_number', 'course']
        labels = {
            'fullname' : 'Ad, soyad',
            'phone_number' : 'Əlaqə nömrəniz',
            'course' : 'Kurs seçin'
        }
        widgets = {
            'fullname' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"",
                }
            ),
            'phone_number' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"+994-- --- -- --"
                }
            ),
            'course' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"Kurs seçin"
                }
            ),
        }
