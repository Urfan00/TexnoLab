import os
from django.db import models
from services.mixins import DateMixin
from ckeditor.fields import RichTextField
from services.uploader import Uploader
from django.template.defaultfilters import slugify
from django.conf import settings
from services.utils import delete_file_if_exists


class Service(DateMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    description1 = RichTextField()
    description2 = RichTextField()
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
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

    class Meta:
        verbose_name = 'Service Home'
        verbose_name_plural = 'Service Home'


class AllGalery(DateMixin):
    img = models.ImageField(upload_to=Uploader.all_galery)

    def __str__(self):
        return f"img-{self.pk}"

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.img))
        
        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        super(AllGalery, self).delete(using, keep_parents)
