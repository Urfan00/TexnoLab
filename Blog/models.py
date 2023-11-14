from django.db import models
from services.mixins import DateMixin
from ckeditor.fields import RichTextField
from services.uploader import Uploader
from django.template.defaultfilters import slugify
from django.conf import settings
from services.utils import delete_file_if_exists
import os
from django.utils.crypto import get_random_string


class BlogCategory(DateMixin):
    name = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'


class Blog(DateMixin):
    title = models.CharField(max_length=255)
    description = RichTextField()
    slug = models.SlugField(null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to=Uploader.blog_category)
    date = models.DateField()
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blog_category')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        while Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            # Generate a unique slug by adding a suffix
            suffix = get_random_string(length=4, allowed_chars='0123456789abcdefghijklmnopqrstuvwxyz')
            self.slug = f"{self.slug}-{suffix}"


        # Check if the instance already exists
        if self.pk:
            old_instance = Blog.objects.get(pk=self.pk)

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

        super(Blog, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
