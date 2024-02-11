from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from Account.models import Account
from Exam.models import CourseTopic
from services.mixins import AuthMentorMixin, AuthTeacherMixin
from .models import LAB, CourseStudent, Group, MentorLabEvaluation, RandomQuestion, StudentResult, TeacherEvaluation
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
from django.db.models import OuterRef, Exists, FloatField, Value, Subquery
from django.db.models.functions import Coalesce



class SaveExamView(View):
    def post(self, request, *args, **kwargs):
        # Assuming the form data is submitted with the group ID (groupId)
        group_id = request.POST.get('groupId')
        exam_durations = request.POST.get('examDuration')
        exam_start_time_str = request.POST.get('startdate')
        course_topic_name = request.POST.get('disabledTopic')

        if group_id and exam_durations and exam_start_time_str and course_topic_name:
            group = get_object_or_404(Group, pk=group_id)
            # Extract and update exam_durations
            # exam_durations = request.POST.get('examDuration')
            if exam_durations:
                group.exam_durations = int(exam_durations)

            # exam_start_time_str = request.POST.get('startdate')
            if exam_start_time_str:
                # Convert the string to a datetime object
                exam_start_time = datetime.strptime(exam_start_time_str, '%Y-%m-%dT%H:%M')
                group.exam_start_time = exam_start_time

            # Extract and update course_topics
            # course_topic_name = request.POST.get('disabledTopic')
            if course_topic_name:
                course_topic = get_object_or_404(CourseTopic, topic_title__icontains=course_topic_name)
                group.course_topic = course_topic

            # Check if the checkbox is checked
            start_end_checkbox = request.POST.get('startEnd')
            if start_end_checkbox == 'true':
                group.is_checked=True
                group.all_course_topics.add(course_topic)

                tt = RandomQuestion.objects.filter(student__learner__group=group).all()
                for t in tt:
                    t.status=False
                    t.save()
                
                ww = StudentResult.objects.filter(student__learner__group=group).all()
                for w in ww:
                    if w.created_at.day != timezone.now().day:
                        w.status=False
                        w.save()

                # Set the status of all students in the group to True
                for account_group in group.student_group.filter(group_student_is_active=True, is_active=False, is_deleted=False):
                    if not StudentResult.objects.filter(student=account_group.student, exam_topics=course_topic).exists():
                        account_group.student.exam_status = True
                        account_group.student.save()
                        account_group.is_exam_group = True
                        account_group.save()
                    else:
                        print('nono')
            elif start_end_checkbox == 'false':
                group.is_checked=False

                # Set the status of all students in the group to False
                for account_group in group.student_group.filter(group_student_is_active=True, is_active=False):
                    account_group.student.exam_status = False
                    account_group.student.save()
                    account_group.is_exam_group = False
                    account_group.save()

            # Save the updated group
            group.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Group ID not provided'})


class ExamStart(AuthTeacherMixin, ListView):
    model = Group
    template_name = 'dshb-forums-1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_account = Account.objects.filter(id=self.request.user.id, staff_status='Müəllim').first()
        teacher_courses = user_account.staff_course.values_list('course', flat=True)
        groups = Group.objects.filter(course__id__in=teacher_courses, is_active=True).all()

        context['topics'] = CourseTopic.objects.filter(course__id__in=teacher_courses, is_deleted=False).all()

        current_time = timezone.now()
        for group in groups:
            if group.exam_end_time and group.exam_end_time < current_time:
                group.is_checked = False
                group.save()
        context["groups"] = groups

        context['current_time'] = current_time

        g_query = self.request.GET.get('state', '')
        if g_query:
            context['all_topics'] = Group.objects.filter(id=g_query, is_active=True).first()

        return context


class TeacherEvaluationView(AuthTeacherMixin, ListView):
    model = Account
    template_name = "dshb-evaluation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_account = Account.objects.filter(id=self.request.user.id, staff_status='Müəllim').first()
        if user_account:
            teacher_courses = user_account.staff_course.values_list('course', flat=True)
            groups = Group.objects.filter(course__id__in=teacher_courses, is_active=True).all()

            context['groups'] = groups

        state = self.request.GET.get('state', '')
        if state:
            today = timezone.now().date()

            context['students'] = CourseStudent.objects.filter(
                group__id=state,
                is_active=False,
                is_deleted=False,
                group_student_is_active=True,
                is_keb=False
            ).annotate(
                new_active=Exists(
                    TeacherEvaluation.objects.filter(
                        student=OuterRef('student'),
                        teacher=self.request.user,
                        updated_at__date=today
                    ).values('id')[:1]
                )
            ).all()


        return context


class GivePointView(View):
    def post(self, request, student_id):
        # Check if the teacher has already given a point to the student today
        today = timezone.now().date()
        teacher = request.user  # Assuming the teacher is the current user
        existing_evaluation = TeacherEvaluation.objects.filter(
            student__id=student_id,
            teacher=teacher,
            updated_at__date=today
        ).first()

        if not existing_evaluation:
            # Create a new evaluation and give 1 point to the student
            evaluation = TeacherEvaluation(student_id=student_id, point=1, teacher=teacher)
            evaluation.save()

        return redirect(request.META.get('HTTP_REFERER'))


class MentorLabEvaluationView(AuthMentorMixin, ListView):
    model = Account
    template_name = "dshb-lab-evaluation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_account = Account.objects.filter(id=self.request.user.id, staff_status='Mentor').first()
        if user_account:
            teacher_courses = user_account.staff_course.values_list('course', flat=True)
            groups = Group.objects.filter(course__id__in=teacher_courses, is_active=True).all()

            context['groups'] = groups
            state = self.request.GET.get('state', '')
            lab = self.request.GET.get('lab', '')
            st = self.request.GET.get('student', '')

            if state:
                students = CourseStudent.objects.filter(
                    group__id=state,
                    is_active=False,
                    is_deleted=False,
                    group_student_is_active=True,
                    is_keb=False
                ).annotate(
                    has_lab_evaluation=Coalesce(
                        Subquery(
                            MentorLabEvaluation.objects.filter(
                                student__id=OuterRef('student__id'),
                                lab__id=lab
                            ).values('point')[:1]
                        ),
                        Value(0),
                        output_field=FloatField()
                    )
                ).all()

                context['students'] = students

                labs = LAB.objects.filter(course__course_group__id=state, is_deleted=False).annotate(
                    lab_points=Coalesce(
                        Subquery(
                            MentorLabEvaluation.objects.filter(
                                lab=OuterRef('pk'), student__id=st
                            ).values('point')[:1]
                        ),
                        Value(0),
                        output_field=FloatField()
                    )
                ).all()

                context['labs'] = labs

            return context


class GiveLabPointView(View):
    def post(self, request):
        student_id = request.POST.get('studentId')
        lab_id = request.POST.get('labId')
        give_points = request.POST.get('give_points')

        student = get_object_or_404(Account, id=student_id)
        lab = get_object_or_404(LAB, id=lab_id)

        existing_entry = MentorLabEvaluation.objects.filter(student=student, lab=lab).first()

        if not existing_entry:
            MentorLabEvaluation.objects.create(
                student=student,
                lab=lab,
                point=give_points,
                mentor=self.request.user,
            )

        return redirect(request.META.get('HTTP_REFERER'))
