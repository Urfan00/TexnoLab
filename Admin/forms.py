from django import forms
from Account.models import Account, Group
from Blog.models import Blog, BlogCategory
from Core.models import FAQ, AboutUs, ContactInfo, Partner
from Course.models import Course, CourseCategory, CourseProgram, CourseStudent, CourseVideo, Gallery, RequestUs
from Service.models import AllGalery, AllVideoGallery, Service, ServiceHome, ServiceImage, ServiceVideo
from multiupload.fields import MultiFileField
from TIM.models import TIMImage, TIMVideo


class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['slug']
        labels = {
            'title' : 'Təlimin başlığı',
            'description' : 'Təlim haqqında',
            'main_photo' : 'Təlimin əsas şəkili',
            'video_link' : 'Video linki',
            'category' : 'Kateqoriya'
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' :"Təlimin başlığı"
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
                    'placeholder' :"http://www",
                    'class' : 'inpClass'
                }
            ),
            'category' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            ),
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
                    'placeholder' :"Xəbər başlığı"
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
                    'type': 'datetime-local',
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
            'title' : 'Xidmət adı',
            'photo' : 'Şəkil',
            'status' : 'Status',
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' :"Xidmət adı"
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


class ServiceImageEditForm(forms.ModelForm):
    photo = MultiFileField(min_num=1, max_num=50, max_file_size=1024*1024*5)

    class Meta:
        model = ServiceImage
        fields = ['photo', 'service']
        widgets = {
            'service' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            )
        }


class ServiceVideoEditForm(forms.ModelForm):
    class Meta:
        model = ServiceVideo
        fields = ['video_url', 'service']
        widgets = {
            'video_url' : forms.URLInput(
                attrs={
                    'placeholder' :"http://www",
                    'class' : 'inpClass'
                }
            ),
            'course' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            )
        }


class CourseVideoEditForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ['video_url', 'course']
        labels = {
            'video_url' : 'Video Url',
            'course' : 'Təlim',
        }
        widgets = {
            'video_url' : forms.URLInput(
                attrs={
                    'placeholder' :"http://www",
                    'class' : 'inpClass'
                }
            ),
            'course' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            )
        }


class AllVideoGalleryEditForm(forms.ModelForm):
    class Meta:
        model = AllVideoGallery
        fields = ['video_url']
        widgets = {
            'video_url' : forms.URLInput(
                attrs={
                    'placeholder' :"http://www",
                    'class' : 'inpClass'
                }
            )
        }


class RequestUsAdminCommentForm(forms.ModelForm):
    class Meta:
        model = RequestUs
        fields = ['admin_comment', 'select_option']
        labels = {
            'admin_comment': 'Admin Şərhi',
            'select_option': 'Status'
        }
        widgets = {
            'admin_comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Şərh yazın",
                    'rows': 8
                }
            ),
            'select_option': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder' :"-seçin-"
                }
            )
        }


class CourseProgramEditForm(forms.ModelForm):
    class Meta:
        model = CourseProgram
        fields = ['program_name', 'description', 'file', 'course']
        labels = {
            'program_name' : 'Proqram başlığı',
            'description' : 'Proqram haqqında',
            'file' : 'Fayl',
            'course' : 'Təlim'
        }
        widgets = {
            'program_name' : forms.TextInput(
                attrs={
                    'placeholder' :"Proqram başlığı"
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
            )
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
                    'placeholder' :"Partner adı"
                }
            )
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
        fields = ['title', 'content', 'img1']
        labels = {
            'title' : 'Başlıq',
            'content' : 'Məzmun',
            'img1' : 'Şəkil 1',
            # 'img2' : 'Şəkil 2',
            # 'img3' : 'Şəkil 3',
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
            )
        }


class ContactInfoEditForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['title', 'location', 'location_url', 'content', 'phone_number', 'email', 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn', 'tiktok', 'whatsapp']
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
            'tiktok': 'TikTok',
            'whatsapp': 'WhatsApp'
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
            'tiktok' : forms.URLInput(
                attrs={
                    'class' : 'inpClass',
                    'placeholder' :"tiktok"
                }
            ),
            'whatsapp' : forms.TextInput(
                attrs={
                    'placeholder' :"+994-- --- -- --"
                }
            )
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


class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'start_date', 'end_date']
        labels = {
            'name' : 'Qrup adı'
        }
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'placeholder' :"Qrup adı"
                }
            ),
            'start_date' : forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder' :"yyyy-dd-mm",
                    'class' : 'inpClass'
                }
            ),
            'end_date' : forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder' :"yyyy-dd-mm",
                    'class' : 'inpClass'
                }
            )
        }


class AllGaleryEditForm(forms.ModelForm):
    img = MultiFileField(min_num=1, max_num=50, max_file_size=1024*1024*5)

    class Meta:
        model = AllGalery
        fields = ['img']


class CourseStudentEditForm(forms.ModelForm):
    class Meta:
        model = CourseStudent
        fields = ['student', 'group', 'course', 'average', 'payment', 'rest', 'rating', 'is_active']
        labels = {
            'student': 'Ad Soyad',
            'group': 'Qrup',
            'course': 'Təlim növü',
            'average': 'Ortalama',
            'payment': 'Ödəniş',
            'rest': 'Qalıq',
            'is_active' : 'Məzun',
            'rating' : 'Reytinq'
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


class GalLeryEditForm(forms.ModelForm):
    photo = MultiFileField(min_num=1, max_num=50, max_file_size=1024*1024*5)

    class Meta:
        model = Gallery
        fields = ['photo', 'course']
        labels = {
            'photo' : 'Şəkil',
            'course' : 'Təlim',
        }
        widgets = {
            'course' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-"
                }
            )
        }


class TIMEditForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description1', 'description2', 'status']
        labels = {
            'title' : 'TİM adı',
            'description1' : 'TİM haqqında 1',
            'description2' : 'TİM haqqında 2',
            'status' : 'Status',
        }
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder' :"TİM adı"
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


class TIMImageEditForm(forms.ModelForm):
    photo = MultiFileField(min_num=1, max_num=50, max_file_size=1024*1024*5)

    class Meta:
        model = TIMImage
        fields = ['photo']


class TIMVideoEditForm(forms.ModelForm):
    class Meta:
        model = TIMVideo
        fields = ['video_url']
        widgets = {
            'video_url' : forms.URLInput(
                attrs={
                    'placeholder' :"http://www",
                    'class' : 'inpClass'
                }
            )
        }
