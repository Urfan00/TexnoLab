from django.db import models
from services.mixins import DateMixin
from ckeditor.fields import RichTextField
from services.uploader import Uploader
from django.template.defaultfilters import slugify


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

    def __str__(self):
        return f'{self.service.title} image {self.pk}'

    class Meta:
        verbose_name = 'Service Image'
        verbose_name_plural = 'Service Images'
