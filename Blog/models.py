from django.db import models
from services.mixins import DateMixin
from ckeditor.fields import RichTextField
from services.uploader import Uploader
from django.template.defaultfilters import slugify


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
    slug = models.SlugField(null=True, blank=True)
    photo = models.ImageField(upload_to=Uploader.blog_category)
    date = models.DateField()
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blog_category')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
