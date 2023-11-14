from django import forms
from Account.models import Account
from Blog.models import Blog, BlogCategory
from Core.models import FAQ, AboutUs, ContactInfo, Partner
from Course.models import Course, CourseCategory, CourseProgram, CourseStudent, RequestUs
from Service.models import AllGalery, Service, ServiceHome
from multiupload.fields import MultiFileField


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
                    "class" : 'inpClass',
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


class ServiceHomeEditForm(forms.ModelForm):
    class Meta:
        model = ServiceHome
        fields = ['title', 'photo', 'status']
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


class FAQEditForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
        labels = {
            'question' : 'Ən çox verilən sual',
            'answer' : 'Cavab'
        }
        widgets = {
            'question' : forms.TextInput(
                attrs={
                    'placeholder' :"sualı qeyd edin"
                }
            ),
            'answer' : forms.TextInput(
                attrs={
                    'placeholder' :"cavabı qeyd edin"
                }
            ),
        }


class AboutUsEditForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = ['title', 'content', 'img1', 'img2', 'img3']
        labels = {
            'title' : 'Başlıq',
            'content' : 'Məzmun',
            'img1' : 'Şəkil1',
            'img2' : 'Şəkil2',
            'img3' : 'Şəkil3',
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' : "Başlıq"
                }
            ),
            'content' : forms.Textarea(
                attrs={
                    'row': "8",
                    'placeholder' : "Məzmun"
                }
            ),
            'img1' : forms.FileInput(
                attrs={
                }
            ),
            'img2' : forms.FileInput(
                attrs={
                }
            ),
            'img3' : forms.FileInput(
                attrs={
                }
            ),
        }


class ContactInfoEditForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['title', 'location', 'location_url', 'content', 'phone_number', 'email', 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn']
        labels = {
            'title' : 'Başlıq',
            'location' : 'Ünvan',
            'location_url' : 'Ünvan linki',
            'content' : 'Məzmun',
            'phone_number' : 'Telefon nömrəsi',
            'email' : 'E-poçt',
            'instagram' : 'İnstagram',
            'twitter' : 'Twitter',
            'facebook' : 'Facebook',
            'github' : 'Github',
            'youtube' : 'YouTube',
            'linkedIn' : 'LinkedIn',
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' :"Başlıq"
                }
            ),
            'location' : forms.TextInput(
                attrs={
                    'placeholder' :"Ünvan"
                }
            ),
            'location_url' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"Ünvan linki"
                }
            ),
            'content' : forms.Textarea(
                attrs={
                    'row': "8",
                    'placeholder' : "Məzmun"
                }
            ),
            'phone_number' : forms.TextInput(
                attrs={
                    'placeholder' :"+994-- --- -- --"
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'placeholder' :"E-poçt"
                }
            ),
            'instagram' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"instagram"
                }
            ),
            'twitter' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"twitter"
                }
            ),
            'facebook' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"facebook"
                }
            ),
            'github' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"github"
                }
            ),
            'youtube' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"youtube"
                }
            ),
            'linkedIn' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"linkedIn"
                }
            ),
        }


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'FIN', 'birthday', 'id_code', 'balance']
        labels = {
            'first_name' : 'Ad',
            'last_name' : 'Soyad',
            'FIN' : 'FİN kod',
            'birthday' : 'Doğum tarixi',
            'id_code' : 'İD Kod',
            'balance' : 'Balans',
        }
        widgets = {
            'first_name' : forms.TextInput(
                attrs={
                    'placeholder' :"Ad"
                }
            ),
            'last_name' : forms.TextInput(
                attrs={
                    'placeholder' :"Soyad"
                }
            ),
            'FIN' : forms.TextInput(
                attrs={
                    'placeholder' :"FİN kod"
                }
            ),
            'birthday' : forms.DateInput(
                attrs={
                    'placeholder' :"yyyy-mm-dd"
                }
            ),
            'id_code' : forms.TextInput(
                attrs={
                    'placeholder' :"İD Kod"
                }
            ),
            'balance' : forms.TextInput(
                attrs={
                    'placeholder' :"Balans"
                }
            ),
        }


class AllGaleryEditForm(forms.ModelForm):
    img = MultiFileField(min_num=1, max_num=50, max_file_size=1024*1024*5)

    class Meta:
        model = AllGalery
        fields = ['img']


class CourseStudentEditForm(forms.ModelForm):
    class Meta:
        model = CourseStudent
        fields = ['student', 'group', 'course', 'average', 'payment', 'rest', 'is_active']
        labels = {
            'student': 'Ad Soyad',
            'group': 'Qrup',
            'course': 'Kurs',
            'average': 'Ortalama',
            'payment': 'Ödəniş',
            'rest': 'Qalıq',
            'is_active' : 'Aktiv'
        }
        widgets = {
            'student' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            ),
            'group' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            ),
            'course' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            ),
            'average' : forms.TextInput(
                attrs={
                    'placeholder' :"Ortalama"
                }
            ),
            'payment' : forms.TextInput(
                attrs={
                    'placeholder' :"Ödəniş"
                }
            ),
            'rest' : forms.TextInput(
                attrs={
                    'placeholder' :"Qalıq"
                }
            ),
        }