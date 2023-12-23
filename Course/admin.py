import os
import shutil
from django.contrib import admin
from .models import Course, CourseCategory, CourseFeedback, CourseProgram, CourseStatistic, CourseStudent, CourseVideo, Gallery, RequestUs



class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'video_url', 'course', 'created_at', 'updated_at']
    search_fields = ['course__title']


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_delete']
    search_fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'main_photo', 'video_link', 'category', 'status', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_filter = ['status', 'is_delete']
    search_fields = ['title', 'slug', 'category__name']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Get the parent directory containing the image
            image_parent_directory = os.path.dirname(obj.main_photo.path)

            # Delete the associated image from the media folder
            if os.path.exists(obj.main_photo.path):
                os.remove(obj.main_photo.path)

            # Delete the object
            obj.delete()

            # Delete the immediate parent directory
            if os.path.exists(image_parent_directory):
                shutil.rmtree(image_parent_directory)

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Course"

    def get_actions(self, request):
        actions = super(CourseAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class CourseFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['is_delete']
    search_fields = ['student', 'course__title']


class RequestUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'select_option', 'phone_number', 'course', 'is_view', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'fullname']
    list_filter = ['is_view', 'is_delete']
    search_fields = ['fullname', 'phone_number', 'course__title']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'course', 'created_at', 'updated_at']
    search_fields = ['course__title']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Delete the associated image from the media folder
            image_path = obj.photo.path
            if os.path.exists(image_path):
                os.remove(image_path)
            # Delete the object
            obj.delete()

            # # Delete the immediate parent directory
            # if os.path.exists(image_parent_directory):
            #     shutil.rmtree(image_parent_directory)

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Request Us"

    def get_actions(self, request):
        actions = super(GalleryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class CourseProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'program_name', 'course', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'program_name',]
    list_filter =  ['is_delete']
    search_fields = ['program_name', 'course__title']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Delete the associated image from the media folder
            image_path = obj.file.path
            if os.path.exists(image_path):
                os.remove(image_path)
            # Delete the object
            obj.delete()

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Course Program"

    def get_actions(self, request):
        actions = super(CourseProgramAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'group', 'course', 'average', 'payment', 'discount', 'rest', 'rating', 'is_keb', 'is_active', 'is_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student__first_name', 'student__last_name', 'student__id_code', 'group__name', 'course__title']
    list_filter = ['rating', 'is_active', 'is_deleted', 'is_keb']


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
admin.site.register(CourseVideo, CourseVideoAdmin)
