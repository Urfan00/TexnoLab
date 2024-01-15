import shutil
from django.db import models
from Account.models import Account
from services.mixins import DateMixin
from services.uploader import Uploader
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.conf import settings
from services.utils import delete_file_if_exists
import os
from django.utils.crypto import get_random_string


class CourseCategory(DateMixin):
    name = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'


class Course(DateMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField()
    main_photo = models.ImageField(upload_to=Uploader.course_main_photo, max_length=255)
    video_link = models.URLField(null=True, blank=True)
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='course_category')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        while Course.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            # Generate a unique slug by adding a suffix
            suffix = get_random_string(length=4, allowed_chars='0123456789abcdefghijklmnopqrstuvwxyz')
            self.slug = f"{self.slug}-{suffix}"

        # Check if the instance already exists
        if self.pk:
            old_instance = Course.objects.get(pk=self.pk)

            # Check if the image field is cleared
            if old_instance.main_photo and not self.main_photo:
                # Delete the old photo file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.main_photo)))

            # Check if the image is changed
            if self.main_photo and self.main_photo != old_instance.main_photo:
                # Delete old image file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.main_photo)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.main_photo))

        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        # Get the parent directory containing the image
        image_parent_directory = os.path.dirname(image_path)

        # Delete the immediate parent directory
        if os.path.exists(image_parent_directory):
            shutil.rmtree(image_parent_directory)

        super(Course, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class TeacherCourse(DateMixin):
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE, limit_choices_to={'staff_status': 'Müəllim'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.id_code} - {self.course.title}"


class CourseFeedback(DateMixin):
    message = models.TextField()
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_course_feedback')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_feedback')
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.first_name} - {self.student.last_name} feedback"

    class Meta:
        verbose_name = 'Course Feedback'
        verbose_name_plural = 'Course Feedback'


class RequestUs(DateMixin):
    select_options = (
        ('seçim 1', 'seçim 1'),
        ('seçim 2', 'seçim 2'),
        ('seçim 3', 'seçim 3'),
        ('seçim 4', 'seçim 4'),
        ('seçim 5', 'seçim 5')
    )
    select_option = models.CharField(choices=select_options, null=True, blank=True, max_length=255)
    admin_comment = models.TextField(null=True, blank=True)
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contact_us')
    is_view = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Request Us'
        verbose_name_plural = 'Request Us'


class Gallery(DateMixin):
    photo = models.ImageField(upload_to=Uploader.course_gallery, max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_gallery')

    def __str__(self):
        return f"{self.course.title} gallery photo {self.pk}"

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = Gallery.objects.get(pk=self.pk)

            # Check if the photo field is cleared
            if old_instance.photo and not self.photo:
                # Delete the old photo file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.photo)))

            # Check if the photo is changed
            if self.photo and self.photo != old_instance.photo:
                # Delete old photo file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.photo)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.photo))

        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        super(Gallery, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'


class CourseProgram(DateMixin):
    program_name = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_program')
    file = models.FileField(upload_to=Uploader.course_program, null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.program_name

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = CourseProgram.objects.get(pk=self.pk)

            # Check if the file field is cleared
            if old_instance.file and not self.file:
                # Delete the old file file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.file)))

                # Set the file field to None
                self.file = None

            # Check if the file is changed
            if self.file and self.file != old_instance.file:
                # Delete old file file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.file)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Delete the file file if it exists
        delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(self.file)))

        super(CourseProgram, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Course Program'
        verbose_name_plural = 'Course Programs'


class CourseStatistic(DateMixin):
    course = models.ForeignKey(Course, on_delete= models.CASCADE, related_name='course_static')
    read_count = models.PositiveIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.course.title} - statistic'

    verbose_name = 'Course Statistic'
    verbose_name_plural = 'Course Statistic'


class CourseVideo(DateMixin):
    video_url = models.URLField(max_length=200, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_video')

    def __str__(self):
        return f'Course Video {self.pk}'

    class Meta:
        verbose_name = 'Course Video'
        verbose_name_plural = 'Course Video'
