import os
from django.db import models
from services.mixins import DateMixin
from ckeditor.fields import RichTextField
from services.uploader import Uploader
from django.template.defaultfilters import slugify
from django.conf import settings
from services.utils import delete_file_if_exists
from django.utils.crypto import get_random_string


class TIM(DateMixin):
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

        while TIM.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
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

        super(TIM, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'TIM'
        verbose_name_plural = 'TIM'


class TIMImage(DateMixin):
    photo = models.ImageField(upload_to=Uploader.tim_image, max_length=255)

    def __str__(self):
        return f'TIM image {self.pk}'

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = TIMImage.objects.get(pk=self.pk)

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

        super(TIMImage, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'TIM Image'
        verbose_name_plural = 'TIM Images'


class TIMVideo(DateMixin):
    video_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'TIM Video {self.pk}'

    class Meta:
        verbose_name = 'TIM Video'
        verbose_name_plural = 'TIM Video'
