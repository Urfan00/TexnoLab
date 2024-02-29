import os
from django.contrib import admin
from .models import TIM, TIMImage, TIMVideo
from import_export.admin import ImportExportModelAdmin



class TIMVideoAdmin(ImportExportModelAdmin):
    list_display = ['id', 'video_url', 'created_at', 'updated_at']


class TIMImageAdmin(ImportExportModelAdmin):
    list_display = ['id', 'photo', 'created_at', 'updated_at']
    # actions = ['delete_selected_with_images']

    # def delete_selected_with_images(self, request, queryset):
    #     for obj in queryset:
    #         # Delete the associated image from the media folder
    #         image_path = obj.photo.path
    #         if os.path.exists(image_path):
    #             os.remove(image_path)

    #         # Delete the object
    #         obj.delete()

    #     self.message_user(request, "Selected tim images and their associated images have been deleted.")

    # delete_selected_with_images.short_description = "Delete selected TIM Video"

    # def get_actions(self, request):
    #     actions = super(TIMImageAdmin, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions


class TIMAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'slug', 'status', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'title', 'slug']
    list_filter = ['status', 'is_delete']
    search_fields = ['title']
    # actions = ['delete_selected_with_images']

    # def delete_selected_with_images(self, request, queryset):
    #     for obj in queryset:
    #         # Collect the paths of associated images
    #         image_paths = [image.photo.path for image in obj.tim_image.all()]

    #         # Delete associated images
    #         for image in obj.tim_image.all():
    #             # Get the path to the image file
    #             image_path = image.photo.path

    #             # Delete the image file if it exists
    #             if os.path.exists(image_path):
    #                 os.remove(image_path)

    #             # Delete the ServiceImage instance
    #             image.delete()

    #         # Delete the Service object
    #         obj.delete()

    #         # Delete parent folders of image paths if they are empty
    #         for image_path in image_paths:
    #             folder_path = os.path.dirname(image_path)
    #             if os.path.exists(folder_path) and not os.listdir(folder_path):
    #                 os.rmdir(folder_path)

    #     self.message_user(request, "Selected tims and their associated images have been deleted.")

    # delete_selected_with_images.short_description = "Delete selected TIM"

    # def get_actions(self, request):
    #     actions = super(TIMAdmin, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions


admin.site.register(TIMVideo, TIMVideoAdmin)
admin.site.register(TIMImage, TIMImageAdmin)
admin.site.register(TIM, TIMAdmin)
