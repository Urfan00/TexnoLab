from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from Account.models import Account
from ExamResult.models import CourseStudent, Group
from services.mixins import AuthStudentPageMixin, AuthTeacherMentorMixin, AuthTeacherMixin
from .forms import SxemStudentForm, SxemTeacherMentorForm
from .models import Sxem, SxemImages, SxemStudent, SxemStudentLOCK, TeacherLastSxemPoint
from django.db.models import Exists, OuterRef, Q, F, Max, Case, When, Value, BooleanField, Subquery, OuterRef
from django.views import View
import re


def sort_alphanumeric(strings):
    def convert(text):
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(strings, key=alphanum_key)


class SxemListView(AuthStudentPageMixin, ListView):
    model = Sxem
    template_name = 'dshb-sxem-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        st_course = CourseStudent.objects.filter(
            student = self.request.user,
            is_deleted = False,
            group__course__is_delete = False,
            group__course__category__is_delete = False,
        )

        context['st_course'] = st_course
        context['len_st_course'] = len(st_course)

        if len(st_course) == 1:
            state = st_course[0].group.course.pk
        else:
            state = self.request.GET.get('state', '')

        if state:
            # Ensure that an SxemStudentLOCK instance is created for the student if it doesn't exist
            sxem_lock, created = SxemStudentLOCK.objects.get_or_create(
                student=self.request.user,
                course_id=state
            )

            # Fetching and sorting Sxem objects based on titles
            sxems = Sxem.objects.filter(
                is_deleted=False,
                course=sxem_lock.course
            ).order_by('sxem_title')

            # Extracting only sxem_title
            sxem_titles = [sxem.sxem_title for sxem in sxems]

            # Sorting the sxem_titles using custom sorting logic
            sorted_sxem_titles = sort_alphanumeric(sxem_titles)

            # Storing the sorted sxem_titles in the context
            context["sxems"] = sxems.order_by(
                Case(
                    *[When(sxem_title=title, then=pos) for pos, title in enumerate(sorted_sxem_titles)]
                )
            ).annotate(
                is_pass_student=Exists(
                    sxem_lock.sxem.filter(pk=OuterRef('pk'))
                )
            )

            if created:
                # Assuming first sxem should be associated
                first_sxem = context["sxems"].first()
                if first_sxem:
                    sxem_lock.sxem.add(first_sxem)

            print('==>1 ', context["sxems"])

            last_sxem_student_answer = SxemStudent.objects.filter(student=self.request.user).last()
            if last_sxem_student_answer:
                print('==>2 ', last_sxem_student_answer.sxem)
                print('==>3 ', last_sxem_student_answer.is_pass)


            if last_sxem_student_answer:
                # If the last answered scheme exists
                if last_sxem_student_answer.is_pass:
                    # If the last answered scheme is marked as passed
                    # Find the next scheme after the last answered scheme
                    last_sxem_title = last_sxem_student_answer.sxem.sxem_title
                    try:
                        index = sorted_sxem_titles.index(last_sxem_title)
                        next_sxem_title = sorted_sxem_titles[index + 1]  # Get the title of the next scheme
                        next_sxem = sxems.get(sxem_title=next_sxem_title)  # Get the next scheme object
                        print('==>4 ', next_sxem)
                        # Add the next scheme to the SxemStudentLOCK instance
                        sxem_lock.sxem.add(next_sxem)
                    except IndexError:
                        print("No next scheme found after the last answered scheme.")

        return context


class SxemDetailView(AuthStudentPageMixin, DetailView, CreateView):
    model = Sxem
    template_name = "dshb-sxem-detail.html"
    form_class = SxemStudentForm

    def get_success_url(self):
        # Redirect to the current page after successful form submission
        return reverse('sxem_detail', kwargs={'pk': self.get_object().pk})

    def get_queryset(self):
        queryset = super().get_queryset()

        st_course = CourseStudent.objects.filter(
            student = self.request.user,
            is_deleted = False,
            group__course__is_delete = False,
            group__course__category__is_delete = False,
        )

        annotated_queryset = queryset.filter(
            is_deleted=False,
            course__in=st_course.values('group__course')
        ).annotate(
            has_passed_sxem=Exists(
                SxemStudentLOCK.objects.filter(
                    sxem=OuterRef('pk'),
                    student=self.request.user,
                )
            )
        )
        return annotated_queryset.filter(has_passed_sxem=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sxem_images"] = SxemImages.objects.filter(sxem=self.get_object()).all()
        context['is_exists'] = SxemStudent.objects.filter(
            student = self.request.user,
            sxem=self.get_object(),
            is_student_answer=True,
        ).exists()

        context['sxem_student_answer'] = SxemStudent.objects.filter(student=self.request.user, sxem=self.get_object()).first()

        s_s_answer = SxemStudent.objects.filter(student=self.request.user, sxem=self.get_object()).first()
        if s_s_answer:
            s_s_answer.is_s_notification = False
            s_s_answer.save()
            context['photo'] = s_s_answer

        return context

    def form_valid(self, form):
        # Check if an instance already exists for the current user and sxem
        sxem_student = SxemStudent.objects.filter(student=self.request.user, sxem=self.get_object()).first()
        
        if sxem_student:
            # If instance exists, update it
            form.instance = sxem_student
            form.instance.is_student_answer = True
            form.instance.student_answer = form.cleaned_data['student_answer']
        else:
            # If instance does not exist, create a new one
            form.instance.student = self.request.user
            form.instance.sxem = self.get_object()
            form.instance.is_student_answer = True

        return super().form_valid(form)


class SxemTeacherMentorListView(AuthTeacherMentorMixin, ListView):
    model = SxemStudent
    template_name = 'dshb-sxem-evaluation-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ts_query = self.request.GET.get('ts', '')
        if self.request.user.staff_course.first():
            tm_course = self.request.user.staff_course.first().course

            if tm_course:
                sxem_teacher_mentor = SxemStudent.objects.filter(sxem__course=tm_course).order_by('-created_at').all()

                if ts_query:
                    sxem_teacher_mentor = sxem_teacher_mentor.filter(
                        Q(student__first_name__icontains=ts_query)
                        | Q(student__last_name__icontains=ts_query)
                        | Q(sxem__sxem_title__icontains=ts_query)
                    )

                context["sxem_teacher_mentor"] = sxem_teacher_mentor

        # sxem yekun bal
        user_account = Account.objects.filter(id=self.request.user.id, staff_status='Müəllim').first()
        if user_account:
            teacher_courses = user_account.staff_course.values_list('course', flat=True)
            groups = Group.objects.filter(course__id__in=teacher_courses, is_active=True).all()

            context['groups'] = groups

            state = self.request.GET.get('state', '')
            if state:
                context['students'] = CourseStudent.objects.filter(
                    group__id=state,
                    is_active=False,
                    is_deleted=False,
                    group_student_is_active=True,
                    is_keb=False
                ).annotate(
                    have_point=Subquery(
                        TeacherLastSxemPoint.objects.filter(
                            student=OuterRef('student_id'),  # Assuming student_id is the field name
                            student_group_id=OuterRef('group_id'),  # Assuming group_id is the field name
                        ).order_by('-id').values('last_sxem_point')[:1]
                    )
                ).all()

        return context


class GiveLastSxemPoint(AuthTeacherMixin, View):

    def post(self, request, student_id, group_id):

        teacher = self.request.user

        student_last_sxem_point = request.POST.get('last_sxem_point')

        TeacherLastSxemPoint.objects.create(student_id=student_id, student_group_id=group_id, teacher=teacher, last_sxem_point=student_last_sxem_point)


        return redirect(request.META.get('HTTP_REFERER'))


class SxemTeacherMentorEvaluationView(AuthTeacherMentorMixin, DetailView, UpdateView):
    model = SxemStudent
    template_name = 'dshb-sxem-detail-teacher-mentor.html'
    form_class = SxemTeacherMentorForm
    context_object_name = 'sxem_student'
    success_url = reverse_lazy('sxem_tm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sxem_images"] = SxemImages.objects.filter(sxem=self.get_object().sxem).all()
        return context

    def form_valid(self, form):
        form.instance.teacher_mentor = self.request.user
        # telebeye notification gedir
        form.instance.is_s_notification = True

        if not form.cleaned_data.get('is_pass'):
            form.instance.is_student_answer = False
        else:
            form.instance.is_student_answer = True

            # Fetch and sort the schemes based on titles
            sxems = Sxem.objects.filter(
                is_deleted=False,
                course=form.instance.sxem.course
            ).order_by('sxem_title')

            # Extracting only sxem_title
            sxem_titles = [sxem.sxem_title for sxem in sxems]

            # Define custom title comparison function
            def custom_title_comparison(title):
                return int(title.split()[-1]) if title else 0

            # Sort the titles based on the custom comparison function
            sorted_sxem_titles = sorted(sxem_titles, key=custom_title_comparison)

            next_sxem_title = None
            current_sxem_title = form.instance.sxem.sxem_title

            # Find the next scheme based on the sorted order
            for title in sorted_sxem_titles:
                if custom_title_comparison(title) > custom_title_comparison(current_sxem_title):
                    next_sxem_title = title
                    break

            if next_sxem_title:
                # Get the next scheme object
                next_sxem = sxems.get(sxem_title=next_sxem_title)

                # Add the next scheme to the SxemStudentLOCK
                sxem_lock, _ = SxemStudentLOCK.objects.get_or_create(
                    student=form.instance.student,
                    course=form.instance.sxem.course
                )
                sxem_lock.sxem.add(next_sxem)

        return super().form_valid(form)






        #     # Get the maximum pk of the Sxem associated with the current SxemStudent
        #     max_sxem_pk = SxemStudent.objects.filter(student=form.instance.student).aggregate(Max('sxem'))['sxem__max']

        #     # Get the next Sxem if it exists
        #     next_sxem = Sxem.objects.filter(course=form.instance.sxem.course, pk__gt=max_sxem_pk).order_by('pk').first()
        #     if next_sxem:
        #         # Get or create the SxemStudentLOCK instance for the current student
        #         sxem_lock, _ = SxemStudentLOCK.objects.get_or_create(student=form.instance.student, course=self.get_object().sxem.course)
        #         sxem_lock.sxem.add(next_sxem)

        # return super().form_valid(form)
