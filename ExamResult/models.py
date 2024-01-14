from django.utils import timezone
from django.db import models
from Account.models import Account
from Course.models import Course
from Exam.models import Answer, CourseTopic, Question
from services.mixins import DateMixin



class Group(DateMixin):
    name = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_group')
    course_topic = models.ForeignKey(CourseTopic, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    exam_durations = models.PositiveIntegerField(default=0)
    is_checked = models.BooleanField(default=False)
    exam_start_time = models.DateTimeField(null=True, blank=True)
    exam_end_time = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.exam_durations:
            self.exam_end_time = self.exam_start_time + timezone.timedelta(minutes=self.exam_durations)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Group'


class CourseStudent(DateMixin):
    ratings = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    rating = models.IntegerField(choices=ratings, null=True, blank=True)
    is_keb = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # mezun true // telebe false
    is_deleted = models.BooleanField(default=False)
    average = models.FloatField(default=0)
    payment = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    rest = models.FloatField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='student_group')
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='learner')
    group_student_is_active = models.BooleanField(default=True)

    # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_course')

    def __str__(self):
        return f"{self.student.get_full_name()}"

    class Meta:
        verbose_name = 'Course Student'
        verbose_name_plural = 'Course Students'


class RandomQuestion(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_random_question')
    point_1_question = models.ManyToManyField(Question, related_name='point_1')
    point_2_question = models.ManyToManyField(Question, related_name='point_2')
    point_3_question = models.ManyToManyField(Question, related_name='point_3')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.get_full_name()} random questions"

    class Meta:
        verbose_name = 'Random Question'
        verbose_name_plural = 'Random Question'


class StudentAnswer(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_answer_question')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_question')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='student_answer', null=True, blank=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.student.get_full_name()} answer"

    def save(self, *args, **kwargs):
        if self.answer and self.answer.is_correct:
            self.is_correct = True
        else:
            self.is_correct = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Student Answer'
        verbose_name_plural = 'Student Answer'


class StudentResult(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    point_1 = models.PositiveIntegerField(default=0)
    point_2 = models.PositiveIntegerField(default=0)
    point_3 = models.PositiveIntegerField(default=0)
    total_point = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    exam_topics = models.ForeignKey(CourseTopic, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.total_point = self.point_1 + self.point_2 + self.point_3
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.get_full_name()} result"

    class Meta:
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Result'
