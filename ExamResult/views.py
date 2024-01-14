from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from Exam.models import CourseTopic
from .models import Group, RandomQuestion, StudentResult
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime



class SaveExamView(View):
    def post(self, request, *args, **kwargs):
        # Assuming the form data is submitted with the group ID (groupId)
        group_id = request.POST.get('groupId')

        if group_id:
            group = get_object_or_404(Group, pk=group_id)

            # Extract and update exam_durations
            exam_durations = request.POST.get('examDuration')
            if exam_durations:
                group.exam_durations = int(exam_durations)

            exam_start_time_str = request.POST.get('startdate')
            if exam_start_time_str:
                # Convert the string to a datetime object
                exam_start_time = datetime.strptime(exam_start_time_str, '%Y-%m-%dT%H:%M')
                group.exam_start_time = exam_start_time


            # Extract and update course_topics
            course_topic_id = request.POST.get('state')
            if course_topic_id:
                course_topic = get_object_or_404(CourseTopic, pk=course_topic_id)
                group.course_topic = course_topic

            # Check if the checkbox is checked
            start_end_checkbox = request.POST.get('startEnd')
            if start_end_checkbox == 'on':
                group.is_checked=True

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
            else:
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


class ExamStart(ListView):
    model = Group
    template_name = 'dshb-forums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.filter(is_active=True).all()
        return context

