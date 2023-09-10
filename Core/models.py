from django.db import models
from services.mixins import DateMixin
from services.uploader import Uploader
from ckeditor.fields import RichTextField



class NavMenu(DateMixin):
    menu = models.CharField(max_length=255)
    sub_menu = models.ForeignKey("NavMenu", on_delete=models.CASCADE, related_name='parent_menu')

    def __str__(self):
        return self.menu

    class Meta:
        verbose_name = 'Navbar Menu'
        verbose_name_plural = 'Navbar Menu'


class Partner(DateMixin):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to=Uploader.partners_image)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'


class AboutUs(DateMixin):
    title = models.CharField(max_length=255)
    content = RichTextField()
    img1 = models.ImageField(upload_to=Uploader.about_us)
    img2 = models.ImageField(upload_to=Uploader.about_us)
    img3 = models.ImageField(upload_to=Uploader.about_us)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'


class ContactUs(DateMixin):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    message = models.TextField()

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Contact Info'
        verbose_name_plural = 'Contact Info'
