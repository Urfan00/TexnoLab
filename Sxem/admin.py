from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Sxem, SxemImages, SxemStudent, SxemStudentLOCK



class SxemAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sxem_title', 'course', 'is_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'sxem_title']
    list_filter = ['is_deleted']
    search_fields = ['sxem_title', 'course__title']


class SxemImagesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sxem', 'image', 'created_at', 'updated_at']
    list_display_links = ['id', 'sxem']
    search_fields = ['sxem__sxem_title']


class SxemStudentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'teacher_mentor', 'sxem', 'student_answer', 'teacher_mentor_comment', 'is_pass', 'is_student_answer', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['is_pass', 'is_student_answer']
    search_fields = ['student__first_name', 'student__last_name', 'sxem__sxem_title']


class SxemStudentLOCKAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student']
    list_display_links = ['id', 'student']


admin.site.register(SxemStudentLOCK, SxemStudentLOCKAdmin)
admin.site.register(Sxem, SxemAdmin)
admin.site.register(SxemImages, SxemImagesAdmin)
admin.site.register(SxemStudent, SxemStudentAdmin)
