from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from ExamResult.models import CourseStudent
from services.mixins import AuthStudentPageMixin, AuthTeacherMentorMixin
from .forms import SxemStudentForm, SxemTeacherMentorForm
from .models import Sxem, SxemImages, SxemStudent, SxemStudentLOCK
from django.db.models import Exists, OuterRef, Q, Max



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
                course_id = state
            )

            if created:
                # Assuming first sxem should be associated
                first_sxem = sxem_lock.course.course_sxem.filter(is_deleted=False).first()
                if first_sxem:
                    sxem_lock.sxem.add(first_sxem)

            context["sxems"] = Sxem.objects.filter(
                is_deleted = False,
                course = sxem_lock.course
            ).annotate(
                is_pass_student=Exists(
                    sxem_lock.sxem.filter(pk=OuterRef('pk'))
                )
            )

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

        return context


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

            # Get the maximum pk of the Sxem associated with the current SxemStudent
            max_sxem_pk = SxemStudent.objects.filter(student=form.instance.student).aggregate(Max('sxem'))['sxem__max']
            
            # Get the next Sxem if it exists
            next_sxem = Sxem.objects.filter(course=form.instance.sxem.course, pk__gt=max_sxem_pk).order_by('pk').first()
            if next_sxem:
                # Get or create the SxemStudentLOCK instance for the current student
                sxem_lock, _ = SxemStudentLOCK.objects.get_or_create(student=form.instance.student, course=self.get_object().sxem.course)
                sxem_lock.sxem.add(next_sxem)

        return super().form_valid(form)
