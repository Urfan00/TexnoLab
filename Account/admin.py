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


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

admin.site.register(Account, AccountAdmin)
admin.site.register(Group, GroupAdmin)

