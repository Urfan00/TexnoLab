from django.db import models
from Course.models import Course
from ckeditor.fields import RichTextField
from services.mixins import DateMixin
from services.uploader import Uploader
from django.utils import timezone




class CourseTopicsTest(DateMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course Topics Test'
        verbose_name_plural = 'Course Topics Test'


class CourseTopic(DateMixin):
    topic_title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_topic')
    course_topic_test = models.ManyToManyField(CourseTopicsTest, blank=True)

    def __str__(self):
        return self.topic_title


class Question(DateMixin):
    question_point = (
        (1, 1),
        (2, 2),
        (3, 3)
    )
    question = RichTextField()
    question_image = models.ImageField(upload_to=Uploader.question_image, max_length=255, null=True, blank=True)
    point = models.IntegerField(choices=question_point)
    course_topic_test = models.ForeignKey(CourseTopicsTest, on_delete=models.CASCADE, related_name='course_topic_test_question')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course_topic_test.name}'s question {self.pk}"


class Answer(DateMixin):
    answer = models.CharField( max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answer')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.question}'s answer {self.pk}"
