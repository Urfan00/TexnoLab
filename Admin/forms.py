from django import forms
from Course.models import Course



class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['slug']
        labels = {
            'title' : 'Kursun başlığı',
            'description' : 'Kurs haqqında',
            'main_photo' : 'Kursun əsas şəkili ',
            'video_link' : 'Video linki',
            'start_date' : 'Başlama tarixi',
            'end_date' : 'Bitmə tarixi',
            'category' : 'Kateqoriya'
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' :"Kursun başlığı"
                }
            ),
            'description' : forms.Textarea(
                attrs={
                    'rows' : 8,
                    'placeholder' :"Ətraflı məlumat"
                }
            ),
            'video_link' : forms.URLInput(
                attrs={
                    'placeholder' :"http://www"
                }
            ),
            'category' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            ),
            'start_date' : forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'placeholder' :"yyyy-dd-mm"
                }
            ),
            'end_date' : forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'placeholder' :"yyyy-dd-mm"
                }
            )
        }