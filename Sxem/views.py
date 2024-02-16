from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from ExamResult.models import CourseStudent
from services.mixins import AuthStudentPageMixin
from .forms import SxemStudentForm
from .models import Sxem, SxemImages, SxemStudent
from django.db.models import BooleanField, Case, When, Exists, OuterRef



class SxemListView(AuthStudentPageMixin, ListView):
    model = Sxem
    template_name = 'dshb-sxem-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course_student = CourseStudent.objects.filter(
                student = self.request.user,
                is_keb = False,
                is_active = False,
                is_deleted = False,
                group_student_is_active = True,
                group__is_active = True,
                group__course__status = True,
                group__course__is_delete = False,
            ).first()

        context["sxems"] = Sxem.objects.filter(
            is_deleted = False,
            course = course_student.group.course
        ).annotate(
            is_pass_student=Case(
                When(
                    Exists(
                        SxemStudent.objects.filter(
                            sxem=OuterRef('pk'),
                            student=self.request.user,
                            is_pass=True
                        )
                    ),
                    then=True
                ),
                default=False,
                output_field=BooleanField()
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
        course_student = CourseStudent.objects.filter(
                student = self.request.user,
                is_keb = False,
                is_active = False,
                is_deleted = False,
                group_student_is_active = True,
                group__is_active = True,
                group__course__status = True,
                group__course__is_delete = False,
            ).first()

        annotated_queryset = queryset.filter(
            is_deleted=False,
            course=course_student.group.course
        ).annotate(
            has_passed_sxem=Case(
                When(
                    sxem_student__student=self.request.user,
                    sxem_student__is_pass=True,
                    then=True
                ),
                When(
                    id = course_student.group.course.course_sxem.first().id,
                    then=True
                ),
                default=False,
                output_field=BooleanField()
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

        context['photo'] = SxemStudent.objects.filter(student=self.request.user, sxem=self.get_object()).first()

        return context

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.sxem = self.get_object()
        form.instance.is_student_answer = True
        return super().form_valid(form)
