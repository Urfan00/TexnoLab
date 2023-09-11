from django import forms
from .models import CourseFeedback


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
