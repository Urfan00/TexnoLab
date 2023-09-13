from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from services.mixins import DateMixin
from services.uploader import Uploader
from django.utils.crypto import get_random_string


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
    FIN = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to=Uploader.user_image, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=20)
    birthday = models.DateField(null=True, blank=True)
    balance = models.FloatField(default=0)
    is_graduate = models.BooleanField(default=False)
    feedback = models.TextField(max_length=255, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    linkedIn = models.URLField(max_length=200, null=True, blank=True)
    group = models.ManyToManyField(Group, blank=True)
    username = None

    USERNAME_FIELD = 'id_code'
    REQUIRED_FIELDS = ['email', 'FIN', 'number']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.id_code:
            self.id_code = get_random_string(length=5, allowed_chars='0123456789abcdefghjkmnpqrstuvwxyz')
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
