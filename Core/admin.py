from django.contrib import admin
from .models import Partner



class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'img', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']

admin.site.register(Partner, PartnerAdmin)
