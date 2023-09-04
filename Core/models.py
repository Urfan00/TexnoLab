from django.db import models
from services.mixins import DateMixin
from services.uploader import Uploader



class Partner(DateMixin):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to=Uploader.partners_image)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'


class About(DateMixin):
    pass
