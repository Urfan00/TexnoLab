from django.contrib import admin
from .models import ContactUs, Course, CourseCategory, CourseFeedback, CourseProgram, CourseStudent, Gallery



class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'main_photo', 'video_link', 'start_date', 'end_date', 'category', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'slug', 'category__name']


class CourseFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student', 'course__title']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'phone_number', 'course', 'created_at', 'updated_at']
    list_display_links = ['id', 'fullname']
    search_fields = ['fullname', 'phone_number', 'course__title']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'course', 'created_at', 'updated_at']
    search_fields = ['course__title']


class CourseProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'program_name', 'sub_program_name', 'course', 'created_at', 'updated_at']
    list_display_links = ['id', 'program_name',]
    search_fields = ['program_name', 'course__title']


class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'group', 'course', 'average', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student__first_name', 'student__last_name', 'student__id_code', 'group__name', 'course__title']
    list_filter = ['is_active']


admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseFeedback, CourseFeedbackAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(CourseProgram, CourseProgramAdmin)
admin.site.register(CourseStudent, CourseStudentAdmin)