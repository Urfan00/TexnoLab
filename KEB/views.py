from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from Account.models import Account
from Course.models import Course
from ExamResult.models import CourseStudent
from django.db.models import Count, Case, When, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class KEBView(ListView):
    model = CourseStudent
    template_name = 'keb-list.html'
    paginate_by = 12

    def get_queryset(self):
        course_slug  = self.request.GET.get('c')
        rating = self.request.GET.get('r')
        sort = self.request.GET.get('sort')

        if course_slug and rating:
            queryset = CourseStudent.objects.filter(
                    is_deleted=False,
                    is_active=True,
                    is_keb=True,
                    student__is_delete=False,
                    student__is_superuser=False,
                    group__course__slug = course_slug,
                    rating = rating
                ).order_by('?').all()
        elif course_slug:
            queryset = CourseStudent.objects.filter(
                    is_deleted=False,
                    is_active=True,
                    is_keb=True,
                    student__is_delete=False,
                    student__is_superuser=False,
                    group__course__slug = course_slug
                ).order_by('?').all()
        elif rating:
            queryset = CourseStudent.objects.filter(
                    is_deleted=False,
                    is_active=True,
                    is_keb=True,
                    student__is_delete=False,
                    student__is_superuser=False,
                    rating = rating
                ).order_by('?').all()
        elif sort:
            if sort=='A-Z':
                queryset = CourseStudent.objects.filter(
                        is_deleted=False,
                        is_active=True,
                        is_keb=True,
                        student__is_delete=False,
                        student__is_superuser=False,
                    ).order_by('student__first_name').all()
            elif sort == 'Z-A':
                queryset = CourseStudent.objects.filter(
                        is_deleted=False,
                        is_active=True,
                        is_keb=True,
                        student__is_delete=False,
                        student__is_superuser=False,
                    ).order_by('-student__first_name').all()
        else:
            queryset = CourseStudent.objects.filter(
                    is_deleted=False,
                    is_active=True,
                    is_keb=True,
                    student__is_delete=False,
                    student__is_superuser=False,
                ).all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keb = self.get_queryset()
        context['total_count'] = keb.count()
        context["all_total_count"] = CourseStudent.objects.filter(is_deleted=False, is_active=True, is_keb=True, student__is_delete=False, student__is_superuser=False).count()
        context['courses'] = Course.objects.annotate(
            num_students=Count(
                Case(
                    When(
                        course_group__student_group__is_keb=True,
                        course_group__student_group__is_deleted=False,
                        course_group__student_group__is_active=True,
                        course_group__student_group__student__is_delete=False,
                        course_group__student_group__student__is_superuser=False,
                        then=1
                        ),
                    output_field=IntegerField()
                )
            )
        )
        print(context['courses'])

        # Pagination
        page = self.request.GET.get('page')
        paginator = Paginator(keb, self.paginate_by)

        try:
            keb = paginator.page(page)
        except PageNotAnInteger:
            keb = paginator.page(1)
        except EmptyPage:
            keb = paginator.page(paginator.num_pages)

        context["keb"] = keb
        return context
