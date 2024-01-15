import os
import shutil
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account


class AccountAdmin(BaseUserAdmin):
    list_display = ("id_code", "first_name", "last_name", 'FIN', "email", "number", 'staff_status', "image", 'cv', "birthday", "balance", 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn', 'exam_status', 'feedback_status', 'first_time_login', 'is_delete', "is_active", "is_superuser")
    list_filter = ('staff_status', "is_active", 'is_staff', 'is_delete', 'exam_status', "is_superuser", 'first_time_login', 'feedback_status')
    fieldsets = (
        ("Credential", {'fields': ('id_code', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'number', 'bio', 'staff_status', 'image', 'cv', 'birthday', 'balance', 'first_time_login', 'exam_status', 'feedback_status', 'is_delete', 'feedback', 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            'CREATE NEW USER',
            {
                "classes": ("wide",),
                "fields": ("id_code", "password1", "password2", "first_name", "last_name", 'FIN', "email", "number"),
            },
        ),
    )
    ordering = ['id_code']  # Use a valid field from your model for ordering
    search_fields = ("id_code", "first_name", "last_name", 'FIN', "email", "number")
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            image_fields = ['image', 'cv']
            # Loop through image fields and delete associated images
            for field in image_fields:
                image_file = getattr(obj, field)
                
                if image_file and image_file.name:
                    image_path = image_file.path

                    # Delete the associated image from the media folder
                    if os.path.exists(image_path):
                        os.remove(image_path)

                    # Delete the immediate parent directory
                    image_parent_directory = os.path.dirname(image_path)
                    if os.path.exists(image_parent_directory):
                        shutil.rmtree(image_parent_directory)

            # Delete the object
            obj.delete()

        self.message_user(request, "Selected accounts and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Account"

    def get_actions(self, request):
        actions = super(AccountAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Account, AccountAdmin)
