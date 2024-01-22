import os
import shutil
from django.contrib import admin
from .models import FAQ, AboutUs, Certificate, ContactInfo, ContactUs, HomePageSliderTextIMG, NavMenu, Partner, Subscribe



class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'img', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_filter = ['is_delete']
    search_fields = ['title']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Get the parent directory containing the image
            image_parent_directory = os.path.dirname(obj.img.path)

            # Delete the associated image from the media folder
            if os.path.exists(obj.img.path):
                os.remove(obj.img.path)

            # Delete the object
            obj.delete()

            # Delete the immediate parent directory
            if os.path.exists(image_parent_directory):
                shutil.rmtree(image_parent_directory)

        self.message_user(request, "Selected blogs and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Partner"

    def get_actions(self, request):
        actions = super(PartnerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'img1', 'img2', 'img3', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Replace 'img1', 'img2', 'img3' with the actual field names in your AboutUs model
            image_fields = ['img1', 'img2', 'img3']

            # Loop through image fields and delete associated images
            for field in image_fields:
                image_path = getattr(obj, field).path
                image_parent_directory = os.path.dirname(image_path)

                # Delete the associated image from the media folder
                if os.path.exists(image_path):
                    os.remove(image_path)

                # Delete the immediate parent directory
                if os.path.exists(image_parent_directory):
                    shutil.rmtree(image_parent_directory)

            # Delete the object
            obj.delete()

        self.message_user(request, "Selected items and their associated images have been deleted.")

    delete_selected_with_images.short_description = "Delete selected About Us"

    def get_actions(self, request):
        actions = super(AboutUsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class NavMenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu', 'sub_menu', 'url_link', 'created_at', 'updated_at']
    list_display_links = ['id', 'menu']
    search_fields = ['menu']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'email', 'is_view', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'fullname']
    list_filter = ['is_view', 'is_delete']
    search_fields = ['fullname', 'email']


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'location', 'location_url', 'phone_number', 'email', 'instagram', 'twitter', 'facebook', 'github', 'youtube', 'linkedIn', 'tiktok', 'whatsapp', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_filter = ['is_delete']
    search_fields = ['title']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer', 'is_delete', 'created_at', 'updated_at']
    list_display_links = ['id', 'question']
    list_filter = ['is_delete']
    search_fields = ['question']


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    list_display_links = ['id', 'email']
    search_fields = ['email']


class CertificateAdmin(admin.ModelAdmin):
    list_display = ['id', 'certificate']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Delete the associated image from the media folder
            image_path = obj.certificate.path
            if os.path.exists(image_path):
                os.remove(image_path)

            # Delete the object
            obj.delete()

        self.message_user(request, "Selected certificate have been deleted.")

    delete_selected_with_images.short_description = "Delete selected Certificate"

    def get_actions(self, request):
        actions = super(CertificateAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class HomePageSliderTextIMGAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'img']
    list_display_links = ['id', 'text']
    actions = ['delete_selected_with_images']

    def delete_selected_with_images(self, request, queryset):
        for obj in queryset:
            # Delete the associated image from the media folder
            image_path = obj.img.path
            if os.path.exists(image_path):
                os.remove(image_path)

            # Delete the object
            obj.delete()

        self.message_user(request, "Selected img have been deleted.")

    delete_selected_with_images.short_description = "Delete selected IMG"

    def get_actions(self, request):
        actions = super(HomePageSliderTextIMGAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions



admin.site.register(HomePageSliderTextIMG, HomePageSliderTextIMGAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(NavMenu, NavMenuAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
