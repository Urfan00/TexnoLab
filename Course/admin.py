from django.contrib import admin
from .models import Course, CourseCategory, CourseFeedback, CourseProgram, CourseStatistic, CourseStudent, Gallery, RequestUs



class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_delete']
    search_fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'main_photo', 'video_link', 'start_date', 'end_date', 'category', 'status', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_filter = ['status', 'is_delete']
    search_fields = ['title', 'slug', 'category__name']


class CourseFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['is_delete']
    search_fields = ['student', 'course__title']


class RequestUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'phone_number', 'course', 'is_view', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'fullname']
    list_filter = ['is_view', 'is_delete']
    search_fields = ['fullname', 'phone_number', 'course__title']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'course', 'is_delete', 'created_at', 'updated_at']
    search_fields = ['course__title']
    list_filter = ['is_delete']


class CourseProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'program_name', 'course', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'program_name',]
    list_filter =  ['is_delete']
    search_fields = ['program_name', 'course__title']


class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'group', 'course', 'average', 'payment', 'discount', 'rest', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student__first_name', 'student__last_name', 'student__id_code', 'group__name', 'course__title']
    list_filter = ['is_active']



class CourseStatisticAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'read_count', 'review_count', 'created_at', 'updated_at']
    list_display_links = ['id', 'course']
    search_fields = ['course__title']


admin.site.register(CourseStatistic, CourseStatisticAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseFeedback, CourseFeedbackAdmin)
admin.site.register(RequestUs, RequestUsAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(CourseProgram, CourseProgramAdmin)
admin.site.register(CourseStudent, CourseStudentAdmin)