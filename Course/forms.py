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
            'fullname' : 'Fullname',
            'phone_number' : 'Phone Number',
            'course' : 'Course'
        }
        widgets = {
            'fullname' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"Fullname",
                }
            ),
            'phone_number' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"Phone number"
                }
            ),
            'course' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"Course"
                }
            ),
        }
