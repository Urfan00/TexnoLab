import os
import shutil
from django.contrib import admin
from .models import Blog, BlogCategory



class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_delete']
    search_fields = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'photo', 'date', 'blog_category', 'status', 'is_delete', 'created_at', 'updated_at']
    list_filter = ['status', 'is_delete']
    list_display_links = ['id', 'title', 'slug']
    search_fields = ['title', 'blog_category__name']
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

    delete_selected_with_images.short_description = "Delete selected Account"

    def get_actions(self, request):
        actions = super(BlogAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)

