import os
from django.db import models
from services.mixins import DateMixin
from ckeditor.fields import RichTextField
from services.uploader import Uploader
from django.template.defaultfilters import slugify
from django.conf import settings
from services.utils import delete_file_if_exists
from django.utils.crypto import get_random_string



class Service(DateMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description1 = RichTextField()
    description2 = RichTextField()
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        while Service.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            # Generate a unique slug by adding a suffix
            suffix = get_random_string(length=4, allowed_chars='0123456789abcdefghijklmnopqrstuvwxyz')
            self.slug = f"{self.slug}-{suffix}"

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class ServiceImage(DateMixin):
    photo = models.ImageField(upload_to=Uploader.service_image)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_images')
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.service.title} image {self.pk}'

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = ServiceImage.objects.get(pk=self.pk)

            # Check if the image field is cleared
            if old_instance.photo and not self.photo:
                # Delete the old photo file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.photo)))

            # Check if the image is changed
            if self.photo and self.photo != old_instance.photo:
                # Delete old image file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.photo)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.photo))

        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        super(ServiceImage, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Service Image'
        verbose_name_plural = 'Service Images'


class ServiceHome(DateMixin):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=Uploader.service_image_home)
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = ServiceHome.objects.get(pk=self.pk)

            # Check if the image field is cleared
            if old_instance.photo and not self.photo:
                # Delete the old photo file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.photo)))

            # Check if the image is changed
            if self.photo and self.photo != old_instance.photo:
                # Delete old image file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.photo)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.photo))

        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        super(ServiceHome, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Service Home'
        verbose_name_plural = 'Service Home'


class AllGalery(DateMixin):
    img = models.ImageField(upload_to=Uploader.all_galery)

    def __str__(self):
        return f"img-{self.pk}"

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = AllGalery.objects.get(pk=self.pk)

            # Check if the image field is cleared
            if old_instance.img and not self.img:
                # Delete the old img file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.img)))

            # Check if the image is changed
            if self.img and self.img != old_instance.img:
                # Delete old image file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.img)))

        super().save(*args, **kwargs)
