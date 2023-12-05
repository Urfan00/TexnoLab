import shutil
from django.db import models
from services.mixins import DateMixin
from services.uploader import Uploader
from ckeditor.fields import RichTextField
from django.conf import settings
from services.utils import delete_file_if_exists
import os



class NavMenu(DateMixin):
    menu = models.CharField(max_length=255)
    url_link = models.CharField(max_length=200, null=True, blank=True)
    sub_menu = models.ForeignKey("NavMenu", on_delete=models.CASCADE, related_name='parent_menu', null=True, blank=True)

    def __str__(self):
        return self.menu

    class Meta:
        verbose_name = 'Navbar Menu'
        verbose_name_plural = 'Navbar Menu'


class Partner(DateMixin):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to=Uploader.partners_image, max_length=255)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = Partner.objects.get(pk=self.pk)

            # Check if the image field is cleared
            if old_instance.img and not self.img:
                # Delete the old photo file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.img)))

            # Check if the image is changed
            if self.img and self.img != old_instance.img:
                # Delete old image file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.img)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.img))

        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        # Get the parent directory containing the image
        image_parent_directory = os.path.dirname(image_path)

        # Delete the immediate parent directory
        if os.path.exists(image_parent_directory):
            shutil.rmtree(image_parent_directory)

        super(Partner, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'


class AboutUs(DateMixin):
    title = models.CharField(max_length=255)
    content = RichTextField()
    img1 = models.ImageField(upload_to=Uploader.about_us, max_length=255)
    img2 = models.ImageField(upload_to=Uploader.about_us, max_length=255)
    img3 = models.ImageField(upload_to=Uploader.about_us, max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = AboutUs.objects.get(pk=self.pk)

            # Loop through image fields and check if the images are cleared or changed
            image_fields = ['img1', 'img2', 'img3']
            for field in image_fields:
                old_image = getattr(old_instance, field)
                new_image = getattr(self, field)

                # Check if the image field is cleared
                if old_image and not new_image:
                    # Delete the old photo file
                    delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_image)))

                # Check if the image is changed
                if new_image and new_image != old_image:
                    # Delete old image file if it exists
                    delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_image)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Loop through image fields and delete associated images
        image_fields = ['img1', 'img2', 'img3']
        for field in image_fields:
            image_path = os.path.join(settings.MEDIA_ROOT, str(getattr(self, field)))
            image_parent_directory = os.path.dirname(image_path)

            # Delete the associated image from the media folder
            delete_file_if_exists(image_path)

            # Delete the immediate parent directory
            if os.path.exists(image_parent_directory):
                shutil.rmtree(image_parent_directory)

        super(AboutUs, self).delete(using, keep_parents)


    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'


class ContactUs(DateMixin):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    is_view = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'


class ContactInfo(DateMixin):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=255, null=True, blank=True)
    location_url = models.URLField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    linkedIn = models.URLField(max_length=200, null=True, blank=True)
    tiktok = models.URLField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=50, null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Contact Info'
        verbose_name_plural = 'Contact Info'


class FAQ(DateMixin):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'F.A.Q'
        verbose_name_plural = 'F.A.Q'


class Subscribe(DateMixin):
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribe'
