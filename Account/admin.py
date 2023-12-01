import os
import shutil
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account, Group


class AccountAdmin(BaseUserAdmin):
    list_display = ("id_code", "first_name", "last_name", 'FIN', "email", "number", "image", "birthday", "balance", 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn', 'first_time_login', "is_graduate", 'is_delete', "is_active", "is_superuser")
    list_filter = ("is_active", 'is_staff', 'is_delete', "is_superuser", "is_graduate", 'first_time_login')
    fieldsets = (
        ("Credential", {'fields': ('id_code', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'number', 'bio', 'image', 'birthday', 'balance', 'group', 'first_time_login', 'is_delete', 'is_graduate', 'feedback', 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn')}),
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
            # Check if the image attribute is not None and has a file associated with it
            if obj.image and obj.image.path and os.path.exists(obj.image.path):
                # Get the parent directory containing the image
                image_parent_directory = os.path.dirname(obj.image.path)

                # Delete the associated image from the media folder
                os.remove(obj.image.path)

                # Delete the immediate parent directory
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

class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

admin.site.register(Account, AccountAdmin)
admin.site.register(Group, GroupAdmin)

