from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Answer, Question
from Account.models import Account
from ExamResult.models import CourseStudent, RandomQuestion, StudentAnswer, StudentResult
from django.db.models import F
from django.utils import timezone
from django.contrib import messages



class AuthStudentMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.staff_status == 'Tələbə':
                account_group = CourseStudent.objects.filter(
                    student=request.user,
                    group_student_is_active=True,
                    is_keb = False,
                    is_active = False,
                    is_deleted = False,
                    is_exam_group = True
                ).first()
                if account_group:
                    if account_group.group.is_active and request.user.exam_status:
                        current_time = timezone.now()
                        if account_group.group.exam_start_time < current_time and account_group.group.exam_end_time > current_time:
                            return super().dispatch(request, *args, **kwargs)
                        else:
                            return redirect('student_dashboard')
                    else:
                        print('ok')
                        messages.error(request, 'Məlumatlarınız yenilənmədi')
                        return redirect('student_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                return render(request, '404.html')
        else:
            return redirect('login')


class RuleView(AuthStudentMixin, ListView):
    model = Account
    template_name = 'quiz-rule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["student"] = Account.objects.filter(id_code=self.request.user.id_code).first()

        if not RandomQuestion.objects.filter(student=self.request.user, status=True).exists():
            account_group = CourseStudent.objects.filter(student=self.request.user, group_student_is_active=True, is_exam_group=True).first()

            assigned_1_questions = list(RandomQuestion.objects.filter(student=self.request.user).values_list('point_1_question__pk', flat=True))
            assigned_2_questions = list(RandomQuestion.objects.filter(student=self.request.user).values_list('point_2_question__pk', flat=True))
            assigned_3_questions = list(RandomQuestion.objects.filter(student=self.request.user).values_list('point_3_question__pk', flat=True))

            # Get all questions already assigned to the student
            assigned_question_ids = set(assigned_1_questions + assigned_2_questions + assigned_3_questions)

            if account_group.group.is_active:
                group_course_topics = account_group.group.course_topic.course_topic_test.all()

                one_point = Question.objects.filter(course_topic_test__in=group_course_topics, point=1, is_active=True).exclude(pk__in=assigned_question_ids).order_by('?')[:3]
                two_point = Question.objects.filter(course_topic_test__in=group_course_topics, point=2, is_active=True).exclude(pk__in=assigned_question_ids).order_by('?')[:4]
                three_point = Question.objects.filter(course_topic_test__in=group_course_topics, point=3, is_active=True).exclude(pk__in=assigned_question_ids).order_by('?')[:3]

                if len(one_point) == 3 and len(two_point) == 4 and len(three_point) == 3:
                    random_questions = RandomQuestion.objects.create(student=self.request.user)

                    random_questions.point_1_question.set(one_point)
                    random_questions.point_2_question.set(two_point)
                    random_questions.point_3_question.set(three_point)
                else:
                    context['dont_have_question'] = True
                    print(context['dont_have_question'])

        return context


class QuizView(AuthStudentMixin, ListView):
    model = RandomQuestion
    template_name = 'dshb-quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_questions"] = RandomQuestion.objects.filter(student=self.request.user, status=True).first()
        examTime = CourseStudent.objects.filter(
            student=self.request.user,
            group_student_is_active=True,
            is_keb = False,
            is_active = False,
            is_deleted = False,
            is_exam_group = True,
            group__is_active = True,
        ).first()
        if examTime:
            context['startTime'] = examTime.group.exam_start_time
            context['endTime'] = examTime.group.exam_end_time

        return context

    def post(self, request, *args, **kwargs):
        # Process the submitted form data and save student answers
        student_random_questions = RandomQuestion.objects.filter(student=self.request.user, status=True).first()

        new_point_1_points = 0
        new_point_2_points = 0
        new_point_3_points = 0

        for question in student_random_questions.point_1_question.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id and answer_id.isdigit() and Answer.objects.filter(id=answer_id).exists():
                answer = question.question_answer.get(id=answer_id)
                a = StudentAnswer.objects.create(student=request.user, question=question, answer=answer)
                if a.is_correct:
                    new_point_1_points += 1
            else:
                StudentAnswer.objects.create(student=request.user, question=question)

        for question in student_random_questions.point_2_question.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id and answer_id.isdigit() and Answer.objects.filter(id=answer_id).exists():
                answer = question.question_answer.get(id=answer_id)
                b = StudentAnswer.objects.create(student=request.user, question=question, answer=answer)
                if b.is_correct:
                    new_point_2_points += 1
            else:
                StudentAnswer.objects.create(student=request.user, question=question)

        for question in student_random_questions.point_3_question.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id and answer_id.isdigit() and Answer.objects.filter(id=answer_id).exists():
                answer = question.question_answer.get(id=answer_id)
                c = StudentAnswer.objects.create(student=request.user, question=question, answer=answer)
                if c.is_correct:
                    new_point_3_points += 1
            else:
                StudentAnswer.objects.create(student=request.user, question=question)

        account_group = CourseStudent.objects.filter(
            student=self.request.user,
            group_student_is_active=True,
            is_keb = False,
            is_active = False,
            is_deleted = False,
            is_exam_group = True,
            group__is_active = True,
        ).first()

        print('==>>> @@ >', account_group)
        print('==>>> !! >', account_group.group)
        print('==>>> ?? >', account_group.group.course_topic)
        # Create or update StudentResult
        student_result, created = StudentResult.objects.get_or_create(student=self.request.user, status=True, s_r_group=account_group.group)
        student_result.point_1 = new_point_1_points
        student_result.point_2 = new_point_2_points * 2
        student_result.point_3 = new_point_3_points * 3
        student_result.exam_topics = account_group.group.course_topic
        student_result.save()

        student = Account.objects.get(id=self.request.user.pk)
        student.exam_status = False
        student.save()

        return redirect('exam_result')


class ExamResultView(ListView):
    model = StudentResult
    template_name = 'quiz-result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result"] = StudentResult.objects.filter(student=self.request.user, status=True).annotate(
            percent_point = F('total_point') * 5
        ).first()
        return context

