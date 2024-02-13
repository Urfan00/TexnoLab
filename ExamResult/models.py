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
    all_course_topics = models.ManyToManyField(CourseTopic, blank=True, related_name='all_course_topics')

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
    group_student_is_active = models.BooleanField(default=True) # tələbə bu qrupda aktiv // deaktiv.
    is_exam_group = models.BooleanField(default=False) # imatahn başladılanda seçilən qrupdursa true olur

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
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='result_student')
    point_1 = models.PositiveIntegerField(default=0)
    point_2 = models.PositiveIntegerField(default=0)
    point_3 = models.PositiveIntegerField(default=0)
    total_point = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    exam_topics = models.ForeignKey(CourseTopic, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_point = self.point_1 + self.point_2 + self.point_3
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.get_full_name()} result"

    class Meta:
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Result'


class TeacherEvaluation(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_evaluation')
    point = models.PositiveIntegerField(default=0)
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='teacher_evaluation')

    def __str__(self):
        return self.student.get_full_name()

    class Meta:
        verbose_name = 'Teacher Evaluation'
        verbose_name_plural = 'Teacher Evaluation'


class LAB(DateMixin):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lab_course')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MentorLabEvaluation(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_lab_evaluation')
    lab = models.ForeignKey(LAB, on_delete=models.CASCADE, related_name='student_lab')
    point = models.FloatField(default=0)
    mentor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='mentor_lab_evaluation')

    def __str__(self):
        return self.student.get_full_name()

    class Meta:
        verbose_name = 'Mentor Lab Evaluation'
        verbose_name_plural = 'Mentor Lab Evaluation'


class TeacherLastLabPoint(DateMixin):
    student_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lab_point_student_group')
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='last_lab_point_student')
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='last_lab_point_teacher')
    last_lab_point = models.PositiveIntegerField()

    def __str__(self):
        return self.student.get_full_name()

    class Meta:
        verbose_name = 'Teacher Last Lab Point'
        verbose_name_plural = 'Teacher Last Lab Point'
