import shutil
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from services.mixins import DateMixin
from services.uploader import Uploader
from django.utils.crypto import get_random_string
from services.utils import delete_file_if_exists
import os
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, id_code, email=None, FIN=None, number=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        user = self.model(id_code=id_code, email=self.normalize_email(email), FIN=FIN, number=number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_code, email=None, FIN=None, number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if email is None:
            raise ValueError('The Email field must be set for superusers.')

        return self.create_user(id_code, email, FIN, number, password, **extra_fields)


class Group(DateMixin):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Account(AbstractUser):
    id_code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    FIN = models.CharField(max_length=21, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to=Uploader.user_image, null=True, blank=True, max_length=255)
    cv = models.FileField(upload_to=Uploader.user_cv, null=True, blank=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=20)
    birthday = models.DateField(null=True, blank=True)
    balance = models.FloatField(default=0)
    is_graduate = models.BooleanField(default=False)
    feedback = models.TextField(max_length=255, null=True, blank=True)
    feedback_status = models.BooleanField(default=False)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    linkedIn = models.URLField(max_length=200, null=True, blank=True)
    group = models.ManyToManyField(Group, blank=True)
    first_time_login = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'id_code'
    REQUIRED_FIELDS = ['email', 'FIN', 'number']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = Account.objects.get(pk=self.pk)

            file_fields = ['image', 'cv']
            for field in file_fields:
                old_file = getattr(old_instance, field)
                new_file = getattr(self, field)

                # Check if the file field is cleared
                if old_file and not new_file:
                    # Delete the old file file
                    delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_file)))

                    # Set the file field to None
                    setattr(self, field, None)

                # Check if the file is changed
                if new_file and new_file != old_file:
                    # Delete old file file if it exists
                    delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_file)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))

        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        # Get the parent directory containing the image
        image_parent_directory = os.path.dirname(image_path)

        # Delete the immediate parent directory
        if os.path.exists(image_parent_directory):
            shutil.rmtree(image_parent_directory)

        super(Account, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
