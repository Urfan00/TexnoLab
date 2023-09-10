from django.contrib import admin
from .models import AboutUs, NavMenu, Partner



class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'img', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'img1', 'img2', 'img3', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']


class NavMenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu', 'sub_menu', 'created_at', 'updated_at']
    list_display_links = ['id', 'menu']
    search_fields = ['menu']


admin.site.register(Partner, PartnerAdmin)
admin.site.register(NavMenu, NavMenuAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
