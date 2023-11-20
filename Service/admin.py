import os
import shutil
from django.contrib import admin
from .models import AllGalery, Service, ServiceHome, ServiceImage



class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'service', 'is_delete', 'created_at', 'updated_at']
    search_fields = ['service__title']
    list_filter = ['is_delete']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Delete the associated image from the media folder
            image_path = obj.photo.path
            if os.path.exists(image_path):
                os.remove(image_path)

            # Delete the object
            obj.delete()

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Service Image"

    def get_actions(self, request):
        actions = super(ServiceImageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'status', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'title', 'slug']
    list_filter = ['status', 'is_delete']
    search_fields = ['title']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Collect the paths of associated images
            image_paths = [image.photo.path for image in obj.service_images.all()]

            # Delete associated images
            for image in obj.service_images.all():
                # Get the path to the image file
                image_path = image.photo.path

                # Delete the image file if it exists
                if os.path.exists(image_path):
                    os.remove(image_path)

                # Delete the ServiceImage instance
                image.delete()

            # Delete the Service object
            obj.delete()

            # Delete parent folders of image paths if they are empty
            for image_path in image_paths:
                folder_path = os.path.dirname(image_path)
                if os.path.exists(folder_path) and not os.listdir(folder_path):
                    os.rmdir(folder_path)

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Service"

    def get_actions(self, request):
        actions = super(ServiceAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class ServiceHomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'photo', 'status', 'is_delete', 'created_at', 'updated_at']
    search_fields = ['title']
    list_filter = ['status', 'is_delete']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Get the parent directory containing the image
            image_parent_directory = os.path.dirname(obj.photo.path)

            # Delete the associated image from the media folder
            if os.path.exists(obj.photo.path):
                os.remove(obj.photo.path)

            # Delete the object
            obj.delete()

            # Delete the immediate parent directory
            if os.path.exists(image_parent_directory):
                shutil.rmtree(image_parent_directory)

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Service Home"

    def get_actions(self, request):
        actions = super(ServiceHomeAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class AllGaleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'img', 'created_at', 'updated_at']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Delete the associated image from the media folder
            image_path = obj.img.path
            if os.path.exists(image_path):
                os.remove(image_path)
            # Delete the object
            obj.delete()

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected All Galery"

    def get_actions(self, request):
        actions = super(AllGaleryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions



admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceImage, ServiceImageAdmin)
admin.site.register(ServiceHome, ServiceHomeAdmin)
admin.site.register(AllGalery)
