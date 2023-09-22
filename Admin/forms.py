from django import forms
from Blog.models import Blog, BlogCategory
from Core.models import Partner
from Course.models import Course, CourseCategory, CourseProgram, RequestUs
from Service.models import Service



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


class CourseCategoryEditForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ['name']
        labels = {
            'name' : 'Kateqoriya adı'
        }
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'placeholder' :"Kateqoriya adı"
                }
            )
        }


class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['slug']
        labels = {
            'title' : 'Xəbər başlığı',
            'description' : 'Xəbər haqqında',
            'photo' : 'Xəbərin əsas şəkili ',
            'date' : 'Tarixi',
            'status' : 'Status',
            'blog_category' : 'Kateqoriya'
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
            'blog_category' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            ),
            'date' : forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'placeholder' :"yyyy-dd-mm"
                }
            )
        }


class BlogCategoryEditForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name']
        labels = {
            'name' : 'Kateqoriya adı'
        }
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'placeholder' :"Kateqoriya adı"
                }
            )
        }


class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description1', 'description2', 'status']
        labels = {
            'title' : 'Servis adı',
            'description1' : 'Servis haqqında 1',
            'description2' : 'Servis haqqında 2',
            'status' : 'Status',
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' :"Service adı"
                }
            ),
            'description1' : forms.Textarea(
                attrs={
                    'rows' : 8,
                    'placeholder' :"Ətraflı məlumat"
                }
            ),
            'description2' : forms.Textarea(
                attrs={
                    'rows' : 8,
                    'placeholder' :"Ətraflı məlumat"
                }
            ),
        }


class RequestUsAdminCommentForm(forms.ModelForm):
    class Meta:
        model = RequestUs
        fields = ['admin_comment']
        labels = {
            'admin_comment' : 'Admin Şərhi'
        }
        widgets = {
            'admin_comment' : forms.Textarea(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"Şərh yazın",
                    'row': 8
                }
            )
        }


class CourseProgramEditForm(forms.ModelForm):
    class Meta:
        model = CourseProgram
        fields = ['program_name', 'description', 'file', 'course']
        labels = {
            'program_name' : 'Program başlığı',
            'description' : 'Program haqqında',
            'file' : 'Fayl',
            'course' : 'Kurs'
        }
        widgets = {
            'program_name' : forms.TextInput(
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
            'course' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            ),
            'file' : forms.FileInput(
                attrs={
                }
            ),
        }


class PartnerEditForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['title', 'img']
        labels = {
            'title' : 'Partner adı',
            'img' : 'Şəkil'
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' :"Kursun başlığı"
                }
            ),
            'img' : forms.FileInput(
                attrs={
                }
            ),
        }

