import os
import shutil
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

    def delete(self, using=None, keep_parents=False):
        # Delete associated images and their parent folders
        for image in self.service_images.all():
            # Get the path to the image file
            image_path = os.path.join(settings.MEDIA_ROOT, str(image.photo))

            # Delete the image file if it exists
            delete_file_if_exists(image_path)

            # Delete the ServiceImage instance
            image.delete()

            # Delete the parent folder if it's empty
            folder_path = os.path.dirname(image_path)
            if os.path.exists(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)

        super(Service, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class ServiceImage(DateMixin):
    photo = models.ImageField(upload_to=Uploader.service_image, max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_image')

    def __str__(self):
        return f'Service image {self.pk}'

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


class ServiceVideo(DateMixin):
    video_url = models.URLField(max_length=200, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_video')

    def __str__(self):
        return f'Service Video {self.pk}'

    class Meta:
        verbose_name = 'Service Video'
        verbose_name_plural = 'Service Video'


class ServiceHome(DateMixin):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=Uploader.service_image_home, max_length=255)
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

        # Get the parent directory containing the image
        image_parent_directory = os.path.dirname(image_path)

        # Delete the immediate parent directory
        if os.path.exists(image_parent_directory):
            shutil.rmtree(image_parent_directory)

        super(ServiceHome, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Service Home'
        verbose_name_plural = 'Service Home'


class AllGalery(DateMixin):
    img = models.ImageField(upload_to=Uploader.all_galery, max_length=255)

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

    def delete(self, using=None, keep_parents=False):
        # Delete the file only if it exists
        if self.img:
            delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(self.img)))

        super(AllGalery, self).delete(using, keep_parents)


class AllVideoGallery(DateMixin):
    video_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"img-{self.pk}"
