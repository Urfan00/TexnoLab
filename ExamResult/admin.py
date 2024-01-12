from django.contrib import admin
from .models import CourseStudent, Group, RandomQuestion, StudentAnswer, StudentResult
from import_export.admin import ImportExportModelAdmin



class GroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'course', 'exam_durations', 'exam_start_time', 'exam_end_time', 'start_date', 'end_date', 'is_checked', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_active', 'is_checked']
    search_fields = ['name', 'course__title']


class CourseStudentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'group', 'average', 'payment', 'discount', 'rest', 'rating', 'is_keb', 'is_active', 'group_student_is_active', 'is_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student__first_name', 'student__last_name', 'student__id_code', 'group__name', 'group__course__title']
    list_filter = ['rating', 'is_active', 'group_student_is_active', 'is_deleted', 'is_keb']


class RandomQuestionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'status', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['status']
    search_fields = ['student__first_name', 'student__last_name']


class StudentAnswerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'question', 'answer', 'is_correct', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['is_correct']
    search_fields = ['student__first_name', 'student__last_name', 'question__question', 'answer__answer']


class StudentResultAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'point_1', 'point_2', 'point_3', 'total_point', 'status', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student__first_name', 'student__last_name', 'student__email']
    list_filter = ['status']



admin.site.register(StudentResult, StudentResultAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(RandomQuestion, RandomQuestionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(CourseStudent, CourseStudentAdmin)
