import os
from django.db import models
from Account.models import Account
from Course.models import Course
from ExamResult.models import Group
from services.mixins import DateMixin
from services.uploader import Uploader
from django.conf import settings
from services.utils import delete_file_if_exists


class Sxem(DateMixin):
    sxem_title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_sxem')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sxem_title} - {self.course.title}"

    def delete(self, using=None, keep_parents=False):
        # Delete associated images and their parent folders
        for image in self.images_sxem.all():
            # Get the path to the image file
            image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))

            # Delete the image file if it exists
            delete_file_if_exists(image_path)

            # Delete the ServiceImage instance
            image.delete()

            # Delete the parent folder if it's empty
            folder_path = os.path.dirname(image_path)
            if os.path.exists(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)

        super(Sxem, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Sxem'
        verbose_name_plural = 'Sxem'


class SxemImages(DateMixin):
    image = models.ImageField(upload_to=Uploader.sxem_images, max_length=255)
    sxem = models.ForeignKey(Sxem, on_delete=models.CASCADE, related_name='images_sxem')

    def __str__(self):
        return f"{self.sxem.sxem_title} image"

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            old_instance = SxemImages.objects.get(pk=self.pk)

            # Check if the image field is cleared
            if old_instance.image and not self.image:
                # Delete the old photo file
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.image)))

            # Check if the image is changed
            if self.image and self.image != old_instance.image:
                # Delete old image file if it exists
                delete_file_if_exists(os.path.join(settings.MEDIA_ROOT, str(old_instance.image)))

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # Get the path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))

        # Delete the image file if it exists
        delete_file_if_exists(image_path)

        super(SxemImages, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'Sxem Image'
        verbose_name_plural = 'Sxem Images'


class SxemStudent(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_sxem')
    teacher_mentor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='teacher_mentor_sxem', null=True)
    sxem = models.ForeignKey(Sxem, on_delete=models.CASCADE, related_name='sxem_student')
    student_answer = models.ImageField(upload_to=Uploader.answer_sxem_images)
    teacher_mentor_comment = models.TextField(null=True, blank=True)
    is_pass = models.BooleanField(default=False) # true olsa telebe novbeti sxeme kece biler
    is_student_answer = models.BooleanField(default=False) # telebe cavab verib ya yox
    is_s_notification = models.BooleanField(default=False) # teacher or mentor comment yada is passi true edibse true olur daha sonra telebe daxil olsa false olur

    def __str__(self):
        return f"{self.student.get_full_name()} {self.sxem.sxem_title} answer"


class SxemStudentLOCK(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_sxem_lock')
    sxem = models.ManyToManyField(Sxem)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sxem_student_course')

    def __str__(self):
        return self.student.get_full_name()


class TeacherLastSxemPoint(DateMixin):
    student_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sxem_point_student_group')
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='last_sxem_point_student')
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='last_sxem_point_teacher')
    last_sxem_point = models.PositiveIntegerField()

    def __str__(self):
        return self.student.get_full_name()

    class Meta:
        verbose_name = 'Teacher Last Sxem Point'
        verbose_name_plural = 'Teacher Last Sxem Point'
