from django.contrib import admin
from .models import FAQ, AboutUs, ContactInfo, ContactUs, NavMenu, Partner



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


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'email', 'created_at', 'updated_at']
    list_display_links = ['id', 'fullname']
    search_fields = ['fullname', 'email']


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'location', 'location_url', 'phone_number', 'email', 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer', 'created_at', 'updated_at']
    list_display_links = ['id', 'question']
    search_fields = ['question']


admin.site.register(Partner, PartnerAdmin)
admin.site.register(NavMenu, NavMenuAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(FAQ, FAQAdmin)

