from django import forms
from .models import CourseFeedback, RequestUs


class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['message']
        labels = {
            'message' : 'Rəyiniz'
        }
        widgets = {
            'message' : forms.Textarea(
                attrs={
                    'class' : 'form-control',
                    'rows' : 8,
                    'placeholder' :"Rəyinizi bildirin"
                }
            )
        }


class RequestUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequestUsForm, self).__init__(*args, **kwargs)
        self.fields['course'].empty_label = "- təlim seçin -"  # Set default value

    class Meta:
        model = RequestUs
        fields = ['fullname', 'phone_number', 'course']
        labels = {
            'fullname' : 'Ad, soyad',
            'phone_number' : 'Əlaqə nömrəniz',
            'course' : 'Təlim seçin'
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
                    'placeholder' :"+994-- --- -- --",
                    'value': '+994'
                }
            ),
            'course' : forms.Select(
                attrs={
                    'class' : 'form-control',
                }
            ),
        }
