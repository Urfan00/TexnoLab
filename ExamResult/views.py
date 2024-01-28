from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from Account.models import Account
from Exam.models import CourseTopic
from .models import Group, RandomQuestion, StudentResult
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime



class AuthTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is teacher
            if request.user.staff_status == 'Müəllim':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not teacher, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


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
                for account_group in group.student_group.filter(is_active=True):
                    account_group.student.exam_status = True
                    account_group.student.save()
            elif start_end_checkbox == 'false':
                group.is_checked=False

                # Set the status of all students in the group to False
                for account_group in group.student_group.filter(is_active=True):
                    account_group.student.exam_status = False
                    account_group.student.save()

            # Save the updated group
            group.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Group ID not provided'})


# class ExamStart(AuthTeacherMixin, ListView):
#     model = Group
#     template_name = 'dshb-forums.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         user_account = Account.objects.filter(id=self.request.user.id, staff_status='Müəllim').first()
#         teacher_courses = user_account.teachercourse_set.values_list('course', flat=True)
#         groups = Group.objects.filter(course__id__in=teacher_courses, is_active=True).all()

#         current_time = timezone.now()
#         for group in groups:
#             if group.exam_end_time and group.exam_end_time < current_time:
#                 group.is_checked = False
#                 group.save()

#         context["groups"] = groups

#         return context


class ExamStart(AuthTeacherMixin, ListView):
    model = Group
    template_name = 'dshb-forums-1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_account = Account.objects.filter(id=self.request.user.id, staff_status='Müəllim').first()
        teacher_courses = user_account.teachercourse_set.values_list('course', flat=True)
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
