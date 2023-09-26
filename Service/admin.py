from django.contrib import admin
from .models import Service, ServiceImage



class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'service', 'is_delete', 'created_at', 'updated_at']
    search_fields = ['service__title']
    list_filter = ['is_delete']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'status', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'title', 'slug']
    list_filter = ['status', 'is_delete']
    search_fields = ['title']


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceImage, ServiceImageAdmin)
