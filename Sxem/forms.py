from django import forms
from .models import SxemStudent



class SxemStudentForm(forms.ModelForm):

    class Meta:
        model = SxemStudent
        fields = ("student_answer",)

        labels = {
            'student_answer' : 'Şəkil'
        }


class SxemTeacherMentorForm(forms.ModelForm):

    class Meta:
        model = SxemStudent
        fields = ("teacher_mentor_comment", "is_pass")

        labels = {
            'teacher_mentor_comment' : 'QEYD:',
            'is_pass' : 'Keçib?'
        }

        widgets = {
            'teacher_mentor_comment': forms.Textarea(
                attrs={
                    'rows': 7,
                    'placeholder': "Ətraflı məlumat"
                    }
                )
        }
