from django.db import models
from Account.models import Account, Group
from services.mixins import DateMixin
from services.uploader import Uploader
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


class CourseCategory(DateMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'


class Course(DateMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    main_photo = models.ImageField(upload_to=Uploader.course_main_photo)
    video_link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='course_category')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseFeedback(DateMixin):
    message = models.TextField()
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_course_feedback')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_feedback')

    def __str__(self):
        return f"{self.student.first_name} - {self.student.last_name} feedback"

    class Meta:
        verbose_name = 'Course Feedback'
        verbose_name_plural = 'Course Feedback'


class RequestUs(DateMixin):
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    admin_comment = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contact_us')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Request Us'
        verbose_name_plural = 'Request Us'


class Gallery(DateMixin):
    photo = models.ImageField(upload_to=Uploader.course_gallery)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_gallery')

    def __str__(self):
        return f"{self.course.title} gallery photo {self.pk}"

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'


class CourseProgram(DateMixin):
    program_name = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)
    # sub_program_name = models.ForeignKey("CourseProgram", on_delete=models.CASCADE, related_name='course_sub_program_name', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_program')
    file = models.FileField(upload_to=Uploader.course_program, null=True, blank=True)

    def __str__(self):
        return self.program_name

    class Meta:
        verbose_name = 'Course Program'
        verbose_name_plural = 'Course Programs'


class CourseStudent(DateMixin):
    is_active = models.BooleanField(default=False)
    average = models.FloatField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='student_group')
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='learner')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_course')

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"

    class Meta:
        verbose_name = 'Course Student'
        verbose_name_plural = 'Course Students'


class CourseStatistic(DateMixin):
    course = models.ForeignKey(Course, on_delete= models.CASCADE, related_name='course_static')
    read_count = models.PositiveIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.course.title} - statistic'

    verbose_name = 'Course Statistic'
    verbose_name_plural = 'Course Statistic'
