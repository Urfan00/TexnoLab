from django.contrib import admin
from .models import CourseStudent, Group



class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_date', 'end_date']
    search_fields = ['name']


class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'group', 'average', 'payment', 'discount', 'rest', 'rating', 'is_keb', 'is_active', 'is_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student__first_name', 'student__last_name', 'student__id_code', 'group__name', 'course__title']
    list_filter = ['rating', 'is_active', 'is_deleted', 'is_keb']



admin.site.register(Group, GroupAdmin)
admin.site.register(CourseStudent, CourseStudentAdmin)
