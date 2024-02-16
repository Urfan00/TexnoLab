from django import forms
from .models import SxemStudent



class SxemStudentForm(forms.ModelForm):
    
    class Meta:
        model = SxemStudent
        fields = ("student_answer",)

        labels = {
            'student_answer' : 'Şəkil'
        }
